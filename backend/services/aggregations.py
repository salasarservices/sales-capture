"""
All MongoDB aggregation pipelines for analytics views.
"""

FISCAL_MONTH_ORDER = [4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3]
FISCAL_LABELS = {
    4: "Apr'25", 5: "May'25", 6: "Jun'25", 7: "Jul'25",
    8: "Aug'25", 9: "Sep'25", 10: "Oct'25", 11: "Nov'25",
    12: "Dec'25", 1: "Jan'26", 2: "Feb'26", 3: "Mar'26"
}


def build_match(fy: str, branch: str, extra: dict = None) -> dict:
    q = {"fy": fy, "branch": branch}
    if extra:
        q.update(extra)
    return {"$match": q}


def summary_sales_pipeline(fy: str, branch: str, extra_match: dict = None) -> list:
    return [
        build_match(fy, branch, extra_match),
        {
            "$group": {
                "_id": "$cre_rm_accountable",
                "total_enquiries": {"$sum": 1},
                "business_converted": {
                    "$sum": {"$cond": [{"$eq": ["$business_closed", "Yes"]}, 1, 0]}
                },
                "total_premium_converted": {
                    "$sum": {
                        "$cond": [
                            {"$eq": ["$business_closed", "Yes"]},
                            {"$ifNull": ["$premium_potential", 0]},
                            0,
                        ]
                    }
                },
                "business_not_converted": {
                    "$sum": {"$cond": [{"$eq": ["$business_closed", "No"]}, 1, 0]}
                },
            }
        },
        {
            "$addFields": {
                "pct_not_converted": {
                    "$cond": [
                        {"$gt": ["$total_enquiries", 0]},
                        {"$multiply": [
                            {"$divide": ["$business_not_converted", "$total_enquiries"]},
                            100
                        ]},
                        0,
                    ]
                }
            }
        },
        {"$sort": {"_id": 1}},
    ]


def business_conversion_pipeline(fy: str, extra_match: dict = None) -> list:
    match_query = {"fy": fy}
    if extra_match:
        match_query.update(extra_match)
    return [
        {"$match": match_query},
        {
            "$group": {
                "_id": {
                    "month": {"$month": "$date_referred"},
                    "year": {"$year": "$date_referred"},
                },
                "no_of_enquiries": {"$sum": 1},
                "business_converted": {
                    "$sum": {"$cond": [{"$eq": ["$business_closed", "Yes"]}, 1, 0]}
                },
            }
        },
        {
            "$addFields": {
                "percentage_converted": {
                    "$cond": [
                        {"$gt": ["$no_of_enquiries", 0]},
                        {"$multiply": [
                            {"$divide": ["$business_converted", "$no_of_enquiries"]},
                            100
                        ]},
                        0,
                    ]
                }
            }
        },
        {"$sort": {"_id.year": 1, "_id.month": 1}},
    ]


def summary_conversion_pipeline(fy: str, branch: str, extra_match: dict = None) -> list:
    return [
        build_match(fy, branch, extra_match),
        {
            "$group": {
                "_id": "$cre_rm_accountable",
                # Fresh
                "fresh_total": {
                    "$sum": {"$cond": [{"$eq": ["$type_of_proposal", "Fresh"]}, 1, 0]}
                },
                "fresh_converted": {
                    "$sum": {
                        "$cond": [
                            {"$and": [
                                {"$eq": ["$type_of_proposal", "Fresh"]},
                                {"$eq": ["$business_closed", "Yes"]},
                            ]},
                            1, 0,
                        ]
                    }
                },
                "fresh_premium": {
                    "$sum": {
                        "$cond": [
                            {"$and": [
                                {"$eq": ["$type_of_proposal", "Fresh"]},
                                {"$eq": ["$business_closed", "Yes"]},
                            ]},
                            {"$ifNull": ["$premium_potential", 0]}, 0,
                        ]
                    }
                },
                "fresh_brokerage": {
                    "$sum": {
                        "$cond": [
                            {"$and": [
                                {"$eq": ["$type_of_proposal", "Fresh"]},
                                {"$eq": ["$business_closed", "Yes"]},
                            ]},
                            {"$ifNull": ["$tentative_brokerage_12pct", 0]}, 0,
                        ]
                    }
                },
                # Renewal
                "renewal_total": {
                    "$sum": {"$cond": [{"$eq": ["$type_of_proposal", "Renewal"]}, 1, 0]}
                },
                "renewal_converted": {
                    "$sum": {
                        "$cond": [
                            {"$and": [
                                {"$eq": ["$type_of_proposal", "Renewal"]},
                                {"$eq": ["$business_closed", "Yes"]},
                            ]},
                            1, 0,
                        ]
                    }
                },
                "renewal_premium": {
                    "$sum": {
                        "$cond": [
                            {"$and": [
                                {"$eq": ["$type_of_proposal", "Renewal"]},
                                {"$eq": ["$business_closed", "Yes"]},
                            ]},
                            {"$ifNull": ["$premium_potential", 0]}, 0,
                        ]
                    }
                },
                "renewal_brokerage": {
                    "$sum": {
                        "$cond": [
                            {"$and": [
                                {"$eq": ["$type_of_proposal", "Renewal"]},
                                {"$eq": ["$business_closed", "Yes"]},
                            ]},
                            {"$ifNull": ["$tentative_brokerage_12pct", 0]}, 0,
                        ]
                    }
                },
                # Expanded
                "expanded_total": {
                    "$sum": {"$cond": [{"$eq": ["$type_of_proposal", "Expanded"]}, 1, 0]}
                },
                "expanded_converted": {
                    "$sum": {
                        "$cond": [
                            {"$and": [
                                {"$eq": ["$type_of_proposal", "Expanded"]},
                                {"$eq": ["$business_closed", "Yes"]},
                            ]},
                            1, 0,
                        ]
                    }
                },
                "expanded_premium": {
                    "$sum": {
                        "$cond": [
                            {"$and": [
                                {"$eq": ["$type_of_proposal", "Expanded"]},
                                {"$eq": ["$business_closed", "Yes"]},
                            ]},
                            {"$ifNull": ["$premium_potential", 0]}, 0,
                        ]
                    }
                },
                "expanded_brokerage": {
                    "$sum": {
                        "$cond": [
                            {"$and": [
                                {"$eq": ["$type_of_proposal", "Expanded"]},
                                {"$eq": ["$business_closed", "Yes"]},
                            ]},
                            {"$ifNull": ["$tentative_brokerage_12pct", 0]}, 0,
                        ]
                    }
                },
                "total_not_converted": {
                    "$sum": {"$cond": [{"$eq": ["$business_closed", "No"]}, 1, 0]}
                },
            }
        },
        {
            "$addFields": {
                "total_enquiries": {
                    "$add": ["$fresh_total", "$renewal_total", "$expanded_total"]
                },
                "total_premium_converted": {
                    "$add": ["$fresh_premium", "$renewal_premium", "$expanded_premium"]
                },
                "total_brokerage_converted": {
                    "$add": ["$fresh_brokerage", "$renewal_brokerage", "$expanded_brokerage"]
                },
                "fresh_pct": {
                    "$cond": [
                        {"$gt": ["$fresh_total", 0]},
                        {"$multiply": [{"$divide": ["$fresh_converted", "$fresh_total"]}, 100]},
                        0,
                    ]
                },
                "renewal_pct": {
                    "$cond": [
                        {"$gt": ["$renewal_total", 0]},
                        {"$multiply": [{"$divide": ["$renewal_converted", "$renewal_total"]}, 100]},
                        0,
                    ]
                },
                "expanded_pct": {
                    "$cond": [
                        {"$gt": ["$expanded_total", 0]},
                        {"$multiply": [{"$divide": ["$expanded_converted", "$expanded_total"]}, 100]},
                        0,
                    ]
                },
            }
        },
        {
            "$addFields": {
                "pct_not_converted": {
                    "$cond": [
                        {"$gt": ["$total_enquiries", 0]},
                        {"$multiply": [{"$divide": ["$total_not_converted", "$total_enquiries"]}, 100]},
                        0,
                    ]
                }
            }
        },
        {"$sort": {"_id": 1}},
    ]


def sales_funnel_pipeline(fy: str, branch: str, extra_match: dict = None) -> list:
    match_query = {"fy": fy, "branch": branch}
    if extra_match:
        match_query.update(extra_match)
    return [
        {"$match": match_query},
        {
            "$group": {
                "_id": None,
                "total_enquiries": {"$sum": 1},
                "quote_submitted": {
                    "$sum": {"$cond": [{"$eq": ["$quote_submitted", "Yes"]}, 1, 0]}
                },
                "business_closed": {
                    "$sum": {"$cond": [{"$eq": ["$business_closed", "Yes"]}, 1, 0]}
                },
            }
        },
    ]


def kpi_pipeline(fy: str, branch: str, extra_match: dict = None) -> list:
    return [
        build_match(fy, branch, extra_match),
        {
            "$group": {
                "_id": None,
                "total_enquiries": {"$sum": 1},
                "total_converted": {
                    "$sum": {"$cond": [{"$eq": ["$business_closed", "Yes"]}, 1, 0]}
                },
                "total_premium_converted": {
                    "$sum": {
                        "$cond": [
                            {"$eq": ["$business_closed", "Yes"]},
                            {"$ifNull": ["$premium_potential", 0]},
                            0,
                        ]
                    }
                },
                "total_brokerage_converted": {
                    "$sum": {
                        "$cond": [
                            {"$eq": ["$business_closed", "Yes"]},
                            {"$ifNull": ["$tentative_brokerage_12pct", 0]},
                            0,
                        ]
                    }
                },
            }
        },
        {
            "$addFields": {
                "overall_conversion_rate": {
                    "$cond": [
                        {"$gt": ["$total_enquiries", 0]},
                        {"$multiply": [
                            {"$divide": ["$total_converted", "$total_enquiries"]},
                            100,
                        ]},
                        0,
                    ]
                }
            }
        },
    ]
