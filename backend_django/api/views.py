"""
API Views - mirroring original FastAPI endpoints.
Uses MongoDB aggregations directly while keeping all original logic.
"""

import json
from datetime import datetime
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.conf import settings
from django.utils import timezone

from core.database import get_collection
from .models import User, LoginAttempt
from .serializers import (
    EnquirySerializer, EnquiryCreateSerializer, UserSerializer,
    UserCreateSerializer, LoginSerializer, TokenResponseSerializer,
)
from .aggregations import (
    summary_sales_pipeline,
    business_conversion_pipeline,
    summary_conversion_pipeline,
    sales_funnel_pipeline,
    kpi_pipeline,
    FISCAL_MONTH_ORDER,
    FISCAL_LABELS,
)
from .authentication import (
    generate_access_token, generate_refresh_token,
    verify_refresh_token, revoke_refresh_token,
)


class EnquiryViewSet(viewsets.ModelViewSet):
    """ViewSet for enquiry CRUD operations."""
    
    queryset = get_collection("enquiries")
    serializer_class = EnquirySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return MongoDB cursor as queryset."""
        return get_collection("enquiries")
    
    def list(self, request, *args, **kwargs):
        """List enquiries with filters and pagination."""
        fy = request.query_params.get("fy", "2025-26")
        branch = request.query_params.get("branch", "Ahmedabad")
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 25))
        
        match = {"fy": fy, "branch": branch}
        
        # Apply filters
        if cre_rm := request.query_params.getlist("cre_rm"):
            match["cre_rm_accountable"] = {"$in": cre_rm}
        if proposal_types := request.query_params.getlist("type"):
            match["type_of_proposal"] = {"$in": proposal_types}
        if months := request.query_params.getlist("month"):
            match["$expr"] = {"$in": [{"$month": "$date_referred"}, [int(m) for m in months]]}
        if company := request.query_params.get("company"):
            import re
            match["company_name"] = {"$regex": re.escape(company), "$options": "i"}
        
        total = self.queryset.count_documents(match)
        skip = (page - 1) * page_size
        
        cursor = (
            self.queryset
            .find(match)
            .sort([("enquiry_no", 1)])
            .skip(skip)
            .limit(page_size)
        )
        
        results = list(cursor)
        for r in results:
            r["id"] = str(r.pop("_id"))
        
        return Response({
            "count": total,
            "page": page,
            "page_size": page_size,
            "results": results,
        })
    
    def retrieve(self, request, *args, **kwargs):
        """Get single enquiry by ID."""
        try:
            doc = self.queryset.find_one({"_id": kwargs["pk"]})
            if not doc:
                return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
            doc["id"] = str(doc.pop("_id"))
            return Response(doc)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request, *args, **kwargs):
        """Create new enquiry."""
        serializer = EnquiryCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        if data.get("premium_potential"):
            data["tentative_brokerage_12pct"] = round(float(data["premium_potential"]) * 0.12, 2)
        
        data["timestamp"] = timezone.now()
        data["created_at"] = timezone.now()
        data["updated_at"] = timezone.now()
        
        # Get next enquiry number
        last = self.queryset.find_one(sort=[("enquiry_no", -1)])
        data["enquiry_no"] = (last["enquiry_no"] + 1) if last else 1
        
        result = self.queryset.insert_one(data)
        data["id"] = str(result.inserted_id)
        
        return Response(data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        """Update enquiry."""
        try:
            obj_id = kwargs["pk"]
            serializer = EnquiryCreateSerializer(data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            
            if data.get("premium_potential"):
                data["tentative_brokerage_12pct"] = round(float(data["premium_potential"]) * 0.12, 2)
            data["updated_at"] = timezone.now()
            
            result = self.queryset.update_one(
                {"_id": obj_id},
                {"$set": data}
            )
            
            if result.matched_count == 0:
                return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
            
            updated = self.queryset.find_one({"_id": obj_id})
            updated["id"] = str(updated.pop("_id"))
            return Response(updated)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        """Soft delete (mark as deleted) - admin only."""
        if not request.user.is_staff:
            return Response({"detail": "Admin only"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            result = self.queryset.update_one(
                {"_id": kwargs["pk"]},
                {"$set": {"deleted_at": timezone.now(), "is_deleted": True}}
            )
            if result.matched_count == 0:
                return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AnalyticsViewSet(viewsets.ViewSet):
    """ViewSet for analytics endpoints - all aggregation views."""
    
    permission_classes = [IsAuthenticated]
    
    def _get_default_params(self, request):
        return {
            "fy": request.query_params.get("fy", "2025-26"),
            "branch": request.query_params.get("branch", "Ahmedabad"),
        }
    
    @action(detail=False, methods=["get"])
    def kpis(self, request):
        """Get KPI summary."""
        params = self._get_default_params(request)
        pipeline = kpi_pipeline(params["fy"], params["branch"])
        result = list(get_collection("enquiries").aggregate(pipeline))
        
        if not result:
            return Response({
                "total_enquiries": 0,
                "total_converted": 0,
                "overall_conversion_rate": 0.0,
                "total_premium_converted": 0.0,
                "total_brokerage_converted": 0.0,
            })
        
        r = result[0]
        r.pop("_id", None)
        return Response(r)
    
    @action(detail=False, methods=["get"])
    def summary_sales(self, request):
        """Get Summary: Sales Capture (View D)."""
        params = self._get_default_params(request)
        pipeline = summary_sales_pipeline(params["fy"], params["branch"])
        rows = list(get_collection("enquiries").aggregate(pipeline))
        
        if not rows:
            return Response([])
        
        df_data = []
        for r in rows:
            row = {"CRE / RM": r["_id"]}
            row.update({k: v for k, v in r.items() if k != "_id"})
            df_data.append(row)
        
        return Response(df_data)
    
    @action(detail=False, methods=["get"])
    def summary_conversion(self, request):
        """Get Summary: Conversion Ratio (View E)."""
        params = self._get_default_params(request)
        pipeline = summary_conversion_pipeline(params["fy"], params["branch"])
        rows = list(get_collection("enquiries").aggregate(pipeline))
        
        if not rows:
            return Response([])
        
        df_data = []
        for r in rows:
            row = {"CRE / RM": r["_id"]}
            row.update({k: v for k, v in r.items() if k != "_id"})
            df_data.append(row)
        
        return Response(df_data)
    
    @action(detail=False, methods=["get"])
    def business_conversion(self, request):
        """Get Business Conversion Ratio (View C) - monthly."""
        fy = request.query_params.get("fy", "2025-26")
        pipeline = business_conversion_pipeline(fy)
        rows = list(get_collection("enquiries").aggregate(pipeline))
        
        # Build complete 12-month scaffold
        scaffold = {
            m: {"no_of_enquiries": 0, "business_converted": 0, "percentage_converted": 0.0}
            for m in FISCAL_MONTH_ORDER
        }
        
        for r in rows:
            m = r["_id"]["month"]
            if m in scaffold:
                scaffold[m] = {
                    "no_of_enquiries": r["no_of_enquiries"],
                    "business_converted": r["business_converted"],
                    "percentage_converted": r["percentage_converted"],
                }
        
        records = []
        for month_num in FISCAL_MONTH_ORDER:
            d = scaffold[month_num]
            records.append({
                "Month": FISCAL_LABELS[month_num],
                "No. of Enquiries": d["no_of_enquiries"],
                "Business Converted": d["business_converted"],
                "Conversion %": round(d["percentage_converted"], 1),
            })
        
        return Response(records)
    
    @action(detail=False, methods=["get"])
    def sales_funnel(self, request):
        """Get Sales Funnel (View B) with optional filters."""
        params = self._get_default_params(request)
        
        extra_match = {}
        if cre_rm := request.query_params.getlist("cre_rm"):
            extra_match["cre_rm_accountable"] = {"$in": cre_rm}
        if proposal_types := request.query_params.getlist("type"):
            extra_match["type_of_proposal"] = {"$in": proposal_types}
        if months := request.query_params.getlist("month"):
            extra_match["$expr"] = {"$in": [{"$month": "$date_referred"}, [int(m) for m in months]]}
        
        pipeline = sales_funnel_pipeline(params["fy"], params["branch"], extra_match if extra_match else None)
        result = list(get_collection("enquiries").aggregate(pipeline))
        
        if not result:
            return Response({"total_enquiries": 0, "quote_submitted": 0, "business_closed": 0})
        
        r = result[0]
        r.pop("_id", None)
        return Response(r)
    
    @action(detail=False, methods=["get"])
    def filter_options(self, request):
        """Get distinct filter options for frontend."""
        params = self._get_default_params(request)
        base = {"fy": params["fy"], "branch": params["branch"]}
        
        collection = get_collection("enquiries")
        cre_rms = sorted([x for x in collection.distinct("cre_rm_accountable", base) if x])
        proposal_types = sorted([x for x in collection.distinct("type_of_proposal", base) if x])
        requirements = sorted([x for x in collection.distinct("requirement", base) if x])
        
        return Response({
            "cre_rms": cre_rms,
            "proposal_types": proposal_types,
            "requirements": requirements,
        })


class LoginView(generics.GenericAPIView):
    """Login endpoint - returns JWT tokens."""
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        
        # Check for locked account
        login_attempt = LoginAttempt.objects.filter(username=username).first()
        if login_attempt and login_attempt.locked_until and login_attempt.locked_until > timezone.now():
            return Response(
                {"detail": "Account locked. Try again later."},
                status=status.HTTP_423_LOCKED
            )
        
        # Authenticate user
        user = authenticate(username=username, password=password)
        
        if user is None:
            # Track failed attempt
            if login_attempt:
                login_attempt.attempts += 1
                if login_attempt.attempts >= 5:
                    login_attempt.locked_until = timezone.now() + timezone.timedelta(minutes=15)
                login_attempt.last_attempt = timezone.now()
                login_attempt.save()
            else:
                LoginAttempt.objects.create(username=username, attempts=1)
            
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Clear failed attempts on successful login
        if login_attempt:
            login_attempt.delete()
        
        # Generate tokens
        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)
        
        return Response({
            "access": access_token,
            "refresh": refresh_token,
            "user": UserSerializer(user).data,
        })


class RefreshTokenView(generics.GenericAPIView):
    """Refresh access token."""
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("refresh")
        if not token:
            return Response({"detail": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = verify_refresh_token(token)
            access_token = generate_access_token(user)
            return Response({"access": access_token})
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    """Logout - revoke refresh token."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.data.get("refresh")
        if token:
            revoke_refresh_token(token)
        return Response({"detail": "Logged out successfully"})


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for user management - admin only."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ["create", "destroy"]:
            return [IsAuthenticated()]
        return super().get_permissions()
    
    def create(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"detail": "Admin only"}, status=status.HTTP_403_FORBIDDEN)
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)