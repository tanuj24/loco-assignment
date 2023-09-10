class UnitTestCases:

    test_liked_only_event = {'reel_liked_data': [{"event_name": "reel_liked", "timestamp": 1000000004, "server_timestamp": 1000000004, "user_uid": "ML0ZSX", "streamer_uid": "GV24MY5", "reel_uid":"881e4c8b-99af-4156-a325-a2068f5bf873", "category_uid": "bgmi", "origin_platform": "ios", "app_version": "5.7.9", "reel_duration": 100, "like_time": 19}
                                            ],
                        'reel_unliked_data': [{"event_name": "reel_unliked", "timestamp": 1000000003, "server_timestamp": 1000000003, "user_uid": "ML0ZSX", "streamer_uid": "GV24MY5", "reel_uid": "881e4c8b-99af-4156-a325-a2068f5bf873", "category_uid": "bgmi", "origin_platform": "ios", "app_version": "5.7.9", "reel_duration": 100, "unlike_time": 38}
],
                        'reel_watched_data': [{"event_name": "reel_watched", "timestamp": 1000000002, "server_timestamp": 1000000002, "user_uid": "ML0ZSX", "streamer_uid": "GV24MY5", "reel_uid": "881e4c8b-99af-4156-a325-a2068f5bf873", "category_uid": "bgmi", "origin_platform": "ios", "app_version": "5.7.9", "reel_watch_duration": 72, "reel_duration": 100, "replay_count": 2},
                                            {"event_name": "reel_watched", "timestamp": 1000000001, "server_timestamp": 1000000001, "user_uid": "ML0ZSX", "streamer_uid": "GV24MY5", "reel_uid": "881e4c8b-99af-4156-a325-a2068f5bf873", "category_uid": "bgmi", "origin_platform": "ios", "app_version": "5.7.9", "reel_watch_duration": 36, "reel_duration": 100, "replay_count": 1}
],
                        'expected_result': [{'user_uid': 'ML0ZSX',
                                            'reel_uid': '881e4c8b-99af-4156-a325-a2068f5bf873',
                                            'timestamp': 1000000002,
                                            'liked': True,
                                            'unliked': False,
                                            'watched_ratio': 0.72,
                                            'is_interested': True,
                                            'latest_timestamp': 1000000002}]}

    test_unliked_only_event = {'reel_liked_data': [{"event_name": "reel_liked", "timestamp": 1000000003, "server_timestamp": 1000000003, "user_uid": "ML0ZSX", "streamer_uid": "GV24MY5", "reel_uid":"881e4c8b-99af-4156-a325-a2068f5bf873", "category_uid": "bgmi", "origin_platform": "ios", "app_version": "5.7.9", "reel_duration": 100, "like_time": 19}
                                            ],
                        'reel_unliked_data': [{"event_name": "reel_unliked", "timestamp": 1000000004, "server_timestamp": 1000000004, "user_uid": "ML0ZSX", "streamer_uid": "GV24MY5", "reel_uid": "881e4c8b-99af-4156-a325-a2068f5bf873", "category_uid": "bgmi", "origin_platform": "ios", "app_version": "5.7.9", "reel_duration": 100, "unlike_time": 38}
],
                        'reel_watched_data': [{"event_name": "reel_watched", "timestamp": 1000000002, "server_timestamp": 1000000002, "user_uid": "ML0ZSX", "streamer_uid": "GV24MY5", "reel_uid": "881e4c8b-99af-4156-a325-a2068f5bf873", "category_uid": "bgmi", "origin_platform": "ios", "app_version": "5.7.9", "reel_watch_duration": 72, "reel_duration": 100, "replay_count": 2},
                                            {"event_name": "reel_watched", "timestamp": 1000000001, "server_timestamp": 1000000001, "user_uid": "ML0ZSX", "streamer_uid": "GV24MY5", "reel_uid": "881e4c8b-99af-4156-a325-a2068f5bf873", "category_uid": "bgmi", "origin_platform": "ios", "app_version": "5.7.9", "reel_watch_duration": 36, "reel_duration": 100, "replay_count": 1}
],
                        'expected_result': [{'user_uid': 'ML0ZSX',
                                            'reel_uid': '881e4c8b-99af-4156-a325-a2068f5bf873',
                                            'timestamp': 1000000002,
                                            'liked': False,
                                            'unliked': True,
                                            'watched_ratio': 0.72,
                                            'is_interested': False,
                                            'latest_timestamp': 1000000002}]}

    test_watched_only_event = {'reel_liked_data': [{"event_name": "reel_liked", "timestamp": 1000000001, "server_timestamp": 1000000001, "user_uid": "ML0ZSX", "streamer_uid": "GV24MY5", "reel_uid":"881e4c8b-99af-4156-a325-a2068f5bf873", "category_uid": "bgmi", "origin_platform": "ios", "app_version": "5.7.9", "reel_duration": 100, "like_time": 19}
                                            ],
                        'reel_unliked_data': [{"event_name": "reel_unliked", "timestamp": 1000000002, "server_timestamp": 1000000002, "user_uid": "ML0ZSX", "streamer_uid": "GV24MY5", "reel_uid": "881e4c8b-99af-4156-a325-a2068f5bf873", "category_uid": "bgmi", "origin_platform": "ios", "app_version": "5.7.9", "reel_duration": 100, "unlike_time": 38}
],
                        'reel_watched_data': [{"event_name": "reel_watched", "timestamp": 1000000004, "server_timestamp": 1000000004, "user_uid": "ML0ZSX", "streamer_uid": "GV24MY5", "reel_uid": "881e4c8b-99af-4156-a325-a2068f5bf873", "category_uid": "bgmi", "origin_platform": "ios", "app_version": "5.7.9", "reel_watch_duration": 72, "reel_duration": 100, "replay_count": 2},
                                            {"event_name": "reel_watched", "timestamp": 1000000003, "server_timestamp": 1000000003, "user_uid": "ML0ZSX", "streamer_uid": "GV24MY5", "reel_uid": "881e4c8b-99af-4156-a325-a2068f5bf873", "category_uid": "bgmi", "origin_platform": "ios", "app_version": "5.7.9", "reel_watch_duration": 36, "reel_duration": 100, "replay_count": 1}
],
                        'expected_result': [{'user_uid': 'ML0ZSX',
                                            'reel_uid': '881e4c8b-99af-4156-a325-a2068f5bf873',
                                            'timestamp': 1000000004,
                                            'liked': False,
                                            'unliked': False,
                                            'watched_ratio': 0.72,
                                            'is_interested': True,
                                            'latest_timestamp': 1000000004}]}
