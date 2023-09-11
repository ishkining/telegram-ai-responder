from amplitude import BaseEvent, Amplitude


def send_amplitude_event(event: str, user_id: int, amplitude: Amplitude):
    amplitude.track(
        BaseEvent(
            event_type=event,
            user_id=str(user_id),
            event_properties={
                "source": "notification"
            }
        )
    )
