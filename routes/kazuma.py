import json
import logging

from flask import jsonify, request

from routes import app

logger = logging.getLogger(__name__)


@app.route("/efficient-hunter-kazuma", methods=["POST"])
def efficient_hunter_kazuma():
    data = request.get_json()
    result = []

    for entry in data:
        monsters = entry.get("monsters", [])
        if not monsters:
            result.append({"maxGold": 0})
            continue

        dp = [(-monsters[0], 0), (-monsters[0], 0)]

        for i in range(1, len(monsters)):
            keep_prepared = dp[-1][0]
            prepare_new_circle = dp[-2][1] - monsters[i]
            with_circle_prepared = max(keep_prepared, prepare_new_circle)

            stay_in_rear = dp[-1][1]
            attack_and_move = dp[-1][0] + monsters[i]
            without_circle_prepared = max(stay_in_rear, attack_and_move)

            dp.append((with_circle_prepared, without_circle_prepared))

        max_gold = max(dp[-1])
        result.append({"efficiency": max_gold})
    return jsonify(result)
