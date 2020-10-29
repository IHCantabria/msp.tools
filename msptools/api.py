from flask import request
from flask_restplus import Api, Resource, fields
from msptools.result import Result
import msptools
from msptools import utils


def start(apiflask):
    ns = apiflask.namespace("/", description="Marine Spatial Planning")

    @ns.route("/check_api", methods=["GET"])
    class CheckApi(Resource):
        def get(self):
            return "API MSP Tools is up!"

    location = apiflask.model("location", {"lon": fields.Float, "lat": fields.Float})
    specie = apiflask.model(
        "specie",
        {
            "name": fields.String,
            "salinity_min": fields.Float,
            "salinity_max": fields.Float,
            "temperature_min": fields.Float,
            "temperature_max": fields.Float,
        },
    )
    dates = apiflask.model(
        "dates",
        {"ini": fields.String("2015-01-01"), "end": fields.String("2015-03-01")},
    )
    params_biological = apiflask.model(
        "BioParams",
        {
            "point": fields.Nested(location),
            "specie": fields.Nested(specie),
            "dates": fields.Nested(dates),
        },
    )

    @ns.route("/biological", methods=["POST"])
    class Biological(Resource):
        # @ns.marshal_with(params_biological)
        @ns.expect(params_biological)
        def post(self):
            try:
                payload = request.json
                bio_index = msptools.run_biological(payload)
                return Result(
                    Result.OK, "", round(float(bio_index), 2)
                ).to_json()
            except msptools.utils.LandException as lex:
                return Result(Result.FAIL, lex.args[0], -997).to_json()
            except ValueError as vex:
                msg = u"Invalid Parameters: {0}".format(vex.args)
                return Result(Result.FAIL, msg, -998).to_json()
            except Exception as ex:
                msg = u"Error calculating index: {0}".format(ex)
                return Result(Result.FAIL, msg, -999).to_json()

    wave_config = apiflask.model(
        "config",
        {
            "hs_min": fields.Float,
            "hs_max": fields.Float,
            "tp_min": fields.Float,
            "tp_max": fields.Float,
            "cge_min": fields.Float,
        },
    )
    params_wave = apiflask.model(
        "WaveParams",
        {
            "config": fields.Nested(wave_config),
            "point": fields.Nested(location),
            "dates": fields.Nested(dates),
        },
    )

    @ns.route("/wave", methods=["POST"])
    class Wave(Resource):
        @ns.expect(params_wave)
        def post(self):
            try:
                payload = request.json
                wave_index = msptools.run_waveenergy(payload)
                return Result(
                    Result.OK, "", round(float(wave_index), 2)
                ).to_json()
            except msptools.utils.LandException as lex:
                return Result(Result.FAIL, lex.args[0], -997).to_json()
            except ValueError as vex:
                msg = u"Invalid Parameters: {0}".format(vex.args)
                return Result(Result.FAIL, msg, -998).to_json()
            except Exception as ex:
                msg = u"Error calculating index: {0}".format(ex)
                return Result(Result.FAIL, msg, -999).to_json()

    wind_config = apiflask.model(
        "config", {"hs_max": fields.Float, "pow": fields.Float,},
    )
    params_wind = apiflask.model(
        "WaveParams",
        {
            "config": fields.Nested(wind_config),
            "point": fields.Nested(location),
            "dates": fields.Nested(dates),
        },
    )

    @ns.route("/wind", methods=["POST"])
    class Wind(Resource):
        @ns.expect(params_wind)
        def post(self):
            try:
                payload = request.json
                wind_index = msptools.run_windenergy(payload)
                return Result(
                    Result.OK, "", round(float(wind_index), 2)
                ).to_json()
            except msptools.utils.LandException as lex:
                return Result(Result.FAIL, lex.args[0], -997).to_json()
            except ValueError as vex:
                msg = u"Invalid Parameters: {0}".format(vex.args)
                return Result(Result.FAIL, msg, -998).to_json()
            except Exception as ex:
                msg = u"Error calculating index: {0}".format(ex)
            return Result(Result.FAIL, msg, -999).to_json()

    @ns.route("/historical", methods=["POST"])
    class Historical(Resource):
        @ns.expect(params_biological)
        def post(self):
            try:
                payload = request.json
                data_serie = msptools.load_historical_serie(payload)
                return Result(Result.OK, "", data_serie).to_json()
            except Exception as ex:
                msg = u"Error retrieving historical data: {0}".format(ex)
                return Result(Result.FAIL, msg, -999).to_json()
