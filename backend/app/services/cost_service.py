"""Static cost lookup table. Returns cost_usd given model + token counts."""

# (input_per_1M_usd, output_per_1M_usd)
PRICING: dict[str, tuple[float, float]] = {
    # OpenAI
    "gpt-4o": (2.50, 10.00),
    "gpt-4o-mini": (0.15, 0.60),
    "gpt-4-turbo": (10.00, 30.00),
    "gpt-4": (30.00, 60.00),
    "gpt-3.5-turbo": (0.50, 1.50),
    "o1": (15.00, 60.00),
    "o1-mini": (3.00, 12.00),
    "o3-mini": (1.10, 4.40),
    # Anthropic
    "claude-3-5-sonnet": (3.00, 15.00),
    "claude-3-5-haiku": (0.80, 4.00),
    "claude-3-opus": (15.00, 75.00),
    "claude-3-haiku": (0.25, 1.25),
    "claude-3-sonnet": (3.00, 15.00),
    "claude-sonnet-4": (3.00, 15.00),
    "claude-opus-4": (15.00, 75.00),
    "claude-haiku-4": (0.80, 4.00),
    # Gemini
    "gemini-2.0-flash": (0.10, 0.40),
    "gemini-1.5-pro": (1.25, 5.00),
    "gemini-1.5-flash": (0.075, 0.30),
    "gemini-1.0-pro": (0.50, 1.50),
}

# Prefix fallback ordering (longest prefix wins)
PREFIX_FALLBACKS = sorted(
    [
        ("gpt-4o-mini", "gpt-4o-mini"),
        ("gpt-4o", "gpt-4o"),
        ("gpt-4-turbo", "gpt-4-turbo"),
        ("gpt-4", "gpt-4"),
        ("gpt-3.5", "gpt-3.5-turbo"),
        ("o1-mini", "o1-mini"),
        ("o1-", "o1"),
        ("o3-mini", "o3-mini"),
        ("claude-3-5-sonnet", "claude-3-5-sonnet"),
        ("claude-3-5-haiku", "claude-3-5-haiku"),
        ("claude-3-opus", "claude-3-opus"),
        ("claude-3-haiku", "claude-3-haiku"),
        ("claude-3-sonnet", "claude-3-sonnet"),
        ("claude-sonnet-4", "claude-sonnet-4"),
        ("claude-opus-4", "claude-opus-4"),
        ("claude-haiku-4", "claude-haiku-4"),
        ("gemini-2.0-flash", "gemini-2.0-flash"),
        ("gemini-1.5-pro", "gemini-1.5-pro"),
        ("gemini-1.5-flash", "gemini-1.5-flash"),
        ("gemini-1.0-pro", "gemini-1.0-pro"),
        ("gemini-2.0", "gemini-2.0-flash"),
        ("gemini-1.5", "gemini-1.5-pro"),
    ],
    key=lambda x: -len(x[0]),  # longest prefix first
)


def get_pricing(model: str) -> tuple[float, float] | None:
    if not isinstance(model, str) or not model:
        return None
    model_lower = model.lower()
    if model_lower in PRICING:
        return PRICING[model_lower]
    for prefix, canonical in PREFIX_FALLBACKS:
        if model_lower.startswith(prefix):
            return PRICING.get(canonical)
    return None


def calculate_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    pricing = get_pricing(model)
    if pricing is None:
        return 0.0
    input_rate, output_rate = pricing
    cost = (prompt_tokens / 1_000_000) * input_rate + (completion_tokens / 1_000_000) * output_rate
    return round(cost, 8)
