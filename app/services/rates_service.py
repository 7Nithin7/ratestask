from app.extensions import db


class RatesService:
    def __get_slugs(self, slug: str) -> list:
        """
        If the given slug is valid, returns an array containing all the child slugs.
        If the given slug is invalid, returns an empty array.
        """
        slugs = [slug]
        for slug in slugs:
            result = db.session.execute(f"SELECT slug FROM regions WHERE parent_slug='{slug}'")
            for row in result:
                slugs.append(row[0])

        # Check if the input slug is a valid slug name
        if len(slugs) == 1:
            result = db.session.execute(f"SELECT slug FROM regions WHERE slug='{slug}'")
            if next(result, None) is None:
                slugs = []

        return slugs

    def get_rates(self, date_from: str, date_to: str, origin: str, destination: str) -> list:
        """
        Returns a list of prices for the given dates and places.
        If region name is given instead of port code,
        rates are fetched against the ports inside that region as well as any of it's child regions.
        """

        origin_slugs = self.__get_slugs(origin)
        destination_slugs = self.__get_slugs(destination)

        if not origin_slugs and not destination_slugs:
            # Assuming both origin and destination are port codes
            result = db.session.execute(
                f"""SELECT AVG(price), COUNT(price), day FROM prices WHERE
                orig_code='{origin}' AND dest_code='{destination}'
                AND day BETWEEN '{date_from}'AND '{date_to}' GROUP BY day"""
            )
        elif not origin_slugs and destination_slugs:
            # Assuming only origin is a port code
            result = db.session.execute(
                f"""SELECT AVG(price), COUNT(price), day FROM prices JOIN ports on prices.dest_code=ports.code WHERE
                orig_code='{origin}' AND ports.parent_slug in ('{"','".join(destination_slugs)}')
                AND day BETWEEN '{date_from}' AND '{date_to}' GROUP BY day"""
            )
        elif origin_slugs and not destination_slugs:
            # Assuming only destination is a port code
            result = db.session.execute(
                f"""SELECT AVG(price), COUNT(price), day FROM prices JOIN ports on prices.orig_code=ports.code WHERE
                dest_code='{destination}' AND ports.parent_slug in ('{"','".join(origin_slugs)}')
                AND day BETWEEN '{date_from}' AND '{date_to}' GROUP BY day"""
            )
        else:
            # Assuming both origin and destination are slugs
            result = db.session.execute(
                f"""SELECT AVG(price), COUNT(price), day FROM prices JOIN ports p1 on prices.orig_code=p1.code
                JOIN ports p2 on prices.dest_code=p2.code WHERE p1.parent_slug in ('{"','".join(origin_slugs)}')
                AND p2.parent_slug in ('{"','".join(destination_slugs)}')
                AND day BETWEEN '{date_from}' AND '{date_to}' GROUP BY day"""
            )
        rates = []
        for avg_price, count, day in result:
            if count >= 3:
                avg_price = float(avg_price)
            else:
                avg_price = None
            rates.append({"day": day.strftime("%Y-%m-%d"), "average_price": avg_price})
        return rates


rates_service = RatesService()
