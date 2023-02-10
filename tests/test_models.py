"""Test the models."""
import pytest
from aiohttp import ClientSession
from aresponses import ResponsesMockServer

from p1monitor import (
    P1Monitor,
    P1MonitorConnectionError,
    P1MonitorNoDataError,
    Phases,
    Settings,
    SmartMeter,
    WaterMeter,
)

from . import load_fixtures


async def test_smartmeter(aresponses: ResponsesMockServer) -> None:
    """Test request from a P1 Monitor device - SmartMeter object."""
    aresponses.add(
        "127.0.0.1",
        "/api/v1/smartmeter",
        "GET",
        aresponses.Response(
            text=load_fixtures("smartmeter.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with ClientSession() as session:
        client = P1Monitor(host="127.0.0.1", session=session)
        smartmeter: SmartMeter = await client.smartmeter()
        assert smartmeter
        assert smartmeter.gas_consumption == 2289.967
        assert smartmeter.power_consumption == 935
        assert smartmeter.power_production == 0
        assert smartmeter.energy_consumption_high == 2996.141
        assert smartmeter.energy_consumption_low == 5436.256
        assert smartmeter.energy_production_high == 4408.947
        assert smartmeter.energy_production_low == 1575.502
        assert smartmeter.energy_tariff_period == "low"


async def test_phases(aresponses: ResponsesMockServer) -> None:
    """Test request from a P1 Monitor device - Phases object."""
    aresponses.add(
        "127.0.0.1",
        "/api/v1/status",
        "GET",
        aresponses.Response(
            text=load_fixtures("phases.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with ClientSession() as session:
        client = P1Monitor(host="127.0.0.1", session=session)
        phases: Phases = await client.phases()
        assert phases
        assert phases.current_phase_l1 == 4.0
        assert phases.power_consumed_phase_l1 == 863
        assert phases.power_produced_phase_l1 == 0
        assert phases.voltage_phase_l1 == 229.0


async def test_watermeter(aresponses: ResponsesMockServer) -> None:
    """Test request from a P1 Monitor device - WaterMeter object."""
    aresponses.add(
        "127.0.0.1",
        "/api/v2/watermeter/day",
        "GET",
        aresponses.Response(
            text=load_fixtures("watermeter.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with ClientSession() as session:
        client = P1Monitor(host="127.0.0.1", session=session)
        watermeter: WaterMeter = await client.watermeter()
        assert watermeter
        assert watermeter.consumption_day == 128
        assert watermeter.consumption_total == 1640.399
        assert watermeter.pulse_count == 128


async def test_no_watermeter_data_new(aresponses: ResponsesMockServer) -> None:
    """Test no WaterMeter data from P1 Monitor device."""
    aresponses.add(
        "127.0.0.1",
        "/api/v2/watermeter/day",
        "GET",
        aresponses.Response(
            text=load_fixtures("no_data.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with ClientSession() as session:
        client = P1Monitor(host="127.0.0.1", session=session)
        with pytest.raises(P1MonitorNoDataError):
            await client.watermeter()


async def test_no_watermeter_data_old(aresponses: ResponsesMockServer) -> None:
    """Test no WaterMeter data from P1 Monitor device."""
    aresponses.add(
        "127.0.0.1",
        "/api/v2/watermeter/day",
        "GET",
        aresponses.Response(
            status=404,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with ClientSession() as session:
        client = P1Monitor(host="127.0.0.1", session=session)
        with pytest.raises(P1MonitorConnectionError):
            await client.watermeter()


async def test_settings(aresponses: ResponsesMockServer) -> None:
    """Test request from a P1 Monitor device - Settings object."""
    aresponses.add(
        "127.0.0.1",
        "/api/v1/configuration",
        "GET",
        aresponses.Response(
            text=load_fixtures("settings.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with ClientSession() as session:
        client = P1Monitor(host="127.0.0.1", session=session)
        settings: Settings = await client.settings()
        assert settings
        assert settings.gas_consumption_price == 0.86687
        assert settings.energy_consumption_price_high == 0.24388
        assert settings.energy_consumption_price_low == 0.22311
        assert settings.energy_production_price_high == 0.24388
        assert settings.energy_production_price_low == 0.22311
