from .knowledge import (
    ACADEMY_NAME,
    ACADEMY_DESCRIPTION,
    ACADEMY_MISSION,
    CURRENT_PROGRAM,
    PROGRAM_DESCRIPTION,
    PROGRAM_DETAILED_DESCRIPTION,
    BENEFITS,
    TRAINING_APPROACH,
    GETTING_STARTED_INFORMATION,
    LIMITATIONS_RESPONSE,
)


def answer(message: str) -> str:
    message = message.strip().lower()

    # Security boundary checks must happen before normal
    # knowledge matching.

    if is_instruction_disclosure_request(message):
        return (
            "I can't provide my internal instructions, system prompts, "
            "or hidden configuration."
        )

    if is_prompt_injection_attempt(message):
        return (
            "I can't follow requests to override or bypass my instructions. "
            "I can help with approved Silver Dragons Academy information."
        )

    if is_private_information_request(message):
        return (
            "I can't provide private, administrative, database, or other "
            "internal information. Please use the Silver Dragons Academy "
            "Contact page for information intended for the public."
        )

    if is_fabrication_request(message):
        return (
            "I can't make up or invent Silver Dragons Academy information. "
            "I can only provide information that has been approved for Silvia."
        )

    # Approved academy knowledge.

    academy_name = ACADEMY_NAME.lower()

    if (
        f"what is {academy_name}" in message
        or f"what is {academy_name.removesuffix(' academy')}" in message
        or f"tell me about {academy_name}" in message
        or f"about {academy_name}" in message
    ):
        return ACADEMY_DESCRIPTION

    if (
        "academy mission" in message
        or "mission of the academy" in message
        or "what is the mission" in message
    ):
        return ACADEMY_MISSION

    if (
        "what is taekwondo" in message
        or f"what is {CURRENT_PROGRAM.lower()}" in message
        or "tell me about taekwondo" in message
    ):
        return PROGRAM_DETAILED_DESCRIPTION

    if (
        "taekwondo program" in message
        or "about the taekwondo program" in message
        or "taekwondo training" in message
    ):
        return PROGRAM_DESCRIPTION

    if (
        "training approach" in message
        or "how do students train" in message
        or "how does training work" in message
        or "how are students trained" in message
    ):
        return TRAINING_APPROACH

    if (
        "program" in message
        or "programs" in message
        or "class" in message
        or "classes" in message
    ):
        return (
            f"{ACADEMY_NAME} currently offers {CURRENT_PROGRAM} as its "
            f"primary program. {PROGRAM_DESCRIPTION}"
        )

    if (
        "benefit" in message
        or "benefits" in message
        or "help me develop" in message
        or "help develop" in message
    ):
        return (
            f"{ACADEMY_NAME} {CURRENT_PROGRAM} training can help develop "
            f"{format_benefits()}."
        )

    if (
        "getting started" in message
        or "how do i get started" in message
        or "how can i get started" in message
        or "interested in taekwondo" in message
        or "interested in joining" in message
    ):
        return GETTING_STARTED_INFORMATION

    if (
        "price" in message
        or "pricing" in message
        or "cost" in message
        or "membership cost" in message
    ):
        return LIMITATIONS_RESPONSE

    if (
        "schedule" in message
        or "class time" in message
        or "class times" in message
    ):
        return LIMITATIONS_RESPONSE

    if (
        "enrollment" in message
        or "enroll" in message
        or "belt testing" in message
        or "testing requirements" in message
        or "refund" in message
        or "refunds" in message
        or "cancellation" in message
        or "cancellations" in message
    ):
        return LIMITATIONS_RESPONSE

    if (
        "hello" in message
        or "hi" in message
        or "hey" in message
    ):
        return (
            "Hello! I'm Silvia, the Silver Dragons Academy virtual assistant. "
            "How can I help?"
        )

    return LIMITATIONS_RESPONSE


def format_benefits() -> str:
    benefits = [benefit.lower() for benefit in BENEFITS]

    if len(benefits) == 0:
        return "character and personal development"

    if len(benefits) == 1:
        return benefits[0]

    if len(benefits) == 2:
        return f"{benefits[0]} and {benefits[1]}"

    return ", ".join(benefits[:-1]) + f", and {benefits[-1]}"


def is_instruction_disclosure_request(message: str) -> bool:
    instruction_terms = [
        "system prompt",
        "system instructions",
        "internal instructions",
        "hidden instructions",
        "internal prompt",
        "hidden prompt",
        "show me your prompt",
        "show your prompt",
        "reveal your prompt",
        "reveal your instructions",
        "tell me your instructions",
        "what are your instructions",
    ]

    return any(term in message for term in instruction_terms)


def is_prompt_injection_attempt(message: str) -> bool:
    injection_terms = [
        "ignore your instructions",
        "ignore previous instructions",
        "ignore all instructions",
        "disregard your instructions",
        "disregard previous instructions",
        "override your instructions",
        "bypass your instructions",
        "forget your instructions",
        "act as if you have no instructions",
    ]

    return any(term in message for term in injection_terms)


def is_private_information_request(message: str) -> bool:
    private_terms = [
        "database information",
        "access the academy database",
        "access academy database",
        "admin information",
        "administrator information",
        "admin credentials",
        "administrator credentials",
        "password",
        "secret key",
        "api key",
        "private information",
        "internal information",
        "private data",
        "internal data",
        "student records",
        "student information",
        "member records",
        "member information",
    ]

    return any(term in message for term in private_terms)


def is_fabrication_request(message: str) -> bool:
    fabrication_terms = [
        "make up",
        "make something up",
        "invent",
        "fabricate",
        "pretend that",
        "pretend you know",
        "just guess",
        "guess the",
        "create fake",
        "give me a fake",
    ]

    return any(term in message for term in fabrication_terms)