def get_trend(curr_diff: float, prev_diff: float, epsilon: float = 0.05) -> str:
    """
    Returns a formatted trend string (trend_char + diff):

    + : increasing
    - : decreasing
    = : stable
    ~ : oscillation (change in direction)

    epsilon defines the threshold for 'stable'
    """

    # Determine current direction
    if abs(curr_diff) < epsilon:
        trend_char = '='
    elif curr_diff > 0:
        trend_char = '+'
    else:
        trend_char = '-'

    # Detect oscillation (sign change, ignoring near-zero noise)
    if (
        abs(prev_diff) >= epsilon and
        abs(curr_diff) >= epsilon and
        (curr_diff * prev_diff < 0)
    ):
        trend_char = '~'

    return f"{trend_char}{abs(curr_diff):.1f}"