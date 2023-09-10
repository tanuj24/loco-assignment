from pyspark.sql import functions as F

class Clips():
    """Clips class

    Args:
        watched_df (spark Dataframe): Reels Watched Dataframe
        liked_df (spark Dataframe): Reels Liked Dataframe
        unliked_df (spark Dataframe): Reels Unliked Dataframe
    """

    def __init__(self, watched_df, liked_df, unliked_df):
        self.watched_df = watched_df
        self.liked_df = liked_df
        self.unliked_df = unliked_df

    def calculate_watched_info(self):
        """calculate_watched_info

        calculates watch ratio given the application version, origin platform, reel duration, replay count for each reel view
        """
        self.watched_df = self.watched_df.withColumn(
        "watched_ratio",
        F.when(
            ((F.col("origin_platform") == "android") &
            (F.col("app_version") >= "2.3.0")) | (F.col("origin_platform") == "ios"),
            F.col("reel_watch_duration") / F.col("reel_duration")
        ).otherwise(
            F.when(
                (F.col("origin_platform") == "android") &
                (F.col("app_version") < "2.3.0") &
                (F.col("replay_count") > 0),
                (F.col("reel_duration") * F.col("replay_count") + F.col("reel_watch_duration")) / F.col("reel_duration")
            )
        )
    )

    def calculate_liked_events(self):
        """calculate_liked_events

        calculates most recent liked events for each reel view
        """

        self.liked_events = self.liked_df.groupBy("user_uid", "reel_uid").agg(F.max("timestamp").alias("liked_timestamp"))

    def calculate_unliked_events(self):
        """calculate_unliked_events

        calculates most recent unliked events for each reel view
        """
        self.unliked_events = self.unliked_df.groupBy("user_uid", "reel_uid").agg(F.max("timestamp").alias("unliked_timestamp"))

    def calculate_interests(self):
        """calculate_interests

        calculates if a user is interested in a reel.
        for reels liked, it checks if the watch timestamp is either equal to or less than liked timestamp and joins on the same conditioon.
        If liked timestamp is less than watched timestamp, then it means user might have taken back his like.

        for reels unliked, it checks if the watch timestamp is either equal to or less than unliked timestamp and joins on the same conditioon.
        If unliked timestamp is less than watched timestamp, then it means user might have taken back his unlike.

        after joining both dfs with watch ratio watched df, cases have been utilised to find wether a user is actually interested in reel or not.

        returns interests dataframe with each row with reel_uid and user_uid having is_interested True or false at the point of that timestamp.
        """

        self.interests_df = self.watched_df.join(
            self.liked_events,
            (self.watched_df["user_uid"] == self.liked_events["user_uid"]) &
            (self.watched_df["reel_uid"] == self.liked_events["reel_uid"]) &
            (self.watched_df["timestamp"] <= self.liked_events["liked_timestamp"]),
            "left"
        ).join(
            self.unliked_events,
            (self.watched_df["user_uid"] == self.unliked_events["user_uid"]) &
            (self.watched_df["reel_uid"] == self.unliked_events["reel_uid"]) &
            (self.watched_df["timestamp"] <= self.unliked_events["unliked_timestamp"]),
            "left"
        ).withColumn(
            "liked",
            F.when(F.col("liked_timestamp").isNotNull() & (F.col("liked_timestamp") >= F.col("unliked_timestamp")), True).otherwise(False)
        ).withColumn(
            "unliked",
            F.when(F.col("unliked_timestamp").isNotNull() & (F.col("unliked_timestamp") >= F.col("liked_timestamp")), True).otherwise(False)
        ).withColumn(
        "is_interested",
        F.when(
            F.col("unliked"),
            False
        ).otherwise(
            F.when(
                F.col("liked"),
                True
            ).otherwise(
                F.when(
                    (~F.col("liked") & ~F.col("unliked")) &
                    (F.col("watched_ratio") > 0.6),
                    True
                ).otherwise(False)
            )
        )).select(
                self.watched_df["user_uid"],
                self.watched_df["reel_uid"],
                self.watched_df["timestamp"],
                "liked",
                "unliked",
                "watched_ratio",
                "is_interested"
            )

    def get_latest_interests(self):

        """get_latest_interests

        Gets latest is_interested status of user-reel based on latest timestamp of action.

        returns final state of interests_df
        """
        latest_status_df = self.interests_df.groupBy("user_uid", "reel_uid").agg(
                            F.max("timestamp").alias("latest_timestamp")
                        )

        self.interests_df = self.interests_df.join(
                        latest_status_df,
                        (self.interests_df["user_uid"] == latest_status_df["user_uid"]) &
                        (self.interests_df["reel_uid"] == latest_status_df["reel_uid"]) &
                        (self.interests_df["timestamp"] == latest_status_df["latest_timestamp"]),
                        "inner"
                    ).drop(latest_status_df["user_uid"]).drop(latest_status_df["reel_uid"]).drop(latest_status_df["latest_timestamp"])

    def run(self):

        """runs

        Runs the logical workflow of the steps.

        1. calcutate liked events
        2. calcutate unliked events
        3. calcutate watch ratio
        4. calculate interest data based on like, unlike and watched datasets.
        5. calculate final interests results.
        """
        self.calculate_liked_events()
        self.calculate_unliked_events()
        self.calculate_watched_info()
        self.calculate_interests()
        self.get_latest_interests()
