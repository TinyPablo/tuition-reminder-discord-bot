MESSAGES_PL = {
    # ===== AUTOMATED PAYMENT REMINDERS =====
    "reminder_week_before_due": (
        "@everyone 📅 {date}: Zbliża się termin płatności ({amount} zł). "
        "Został tydzień do końca miesiąca — jeśli jeszcze nie zapłaciłeś, przygotuj przelew."
    ),

    "reminder_day_before_due": (
        "@everyone ⚠️ {date}: Ostatni dzień na zwykły przelew ({amount} zł). "
        "Od jutra dostępny będzie już tylko przelew natychmiastowy."
    ),

    "reminder_due_today": (
        "@everyone 🚨 {date}: Termin płatności przypada dziś ({amount} zł). "
        "Jeśli jeszcze nie zrobiłeś przelewu, wykonaj go jako *instant*."
    ),

    # ===== BROADCAST MESSAGES (sent publicly when admin updates config) =====
    "broadcast_normal_payment_changed": (
        "@everyone 🔧 Zmieniono kwotę płatności dla miesięcy zwykłych na **{value} zł**."
    ),

    "broadcast_holiday_payment_changed": (
        "@everyone 🔧 Zmieniono kwotę płatności dla miesięcy wakacyjnych na **{value} zł**."
    ),

    # ===== USER CONFIRMATION MESSAGES (ephemeral, visible only to user) =====
    "confirm_normal_payment_updated": (
        "✅ Kwota płatności dla miesięcy zwykłych została zaktualizowana do **{value} zł**."
    ),
    
    "error_missing_manager_role": (
        "❌ Nie masz uprawnień do wykonania tej komendy. Wymagana rola: <@&{role_id}>."
    ),

    "confirm_holiday_payment_updated": (
        "✅ Kwota płatności dla miesięcy wakacyjnych została zaktualizowana do **{value} zł**."
    ),

    # ===== SYSTEM / INTERNAL MESSAGES =====
    "system_config_saved": "✅ Zapisano konfigurację.",
    
    # ===== VALIDATION ERRORS =====
    "error_amount_must_be_positive": (
        "❌ Podana kwota musi być większa niż 0."
    ),

    "error_amount_same_as_current": (
        "❌ Nowa kwota jest taka sama jak obecna ({current} zł)."
    ),
}