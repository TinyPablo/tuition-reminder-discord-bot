MESSAGES_PL = {
    "reminders": {
        "week_before_due": (
            "@everyone 📅 {date}: Zbliża się termin płatności ({amount} zł). "
            "Został tydzień do końca miesiąca — jeśli jeszcze nie zapłaciłeś, przygotuj przelew."
        ),
        "day_before_due": (
            "@everyone ⚠️ {date}: Ostatni dzień na zwykły przelew ({amount} zł). "
            "Od jutra dostępny będzie już tylko przelew natychmiastowy."
        ),
        "due_today": (
            "@everyone 🚨 {date}: Termin płatności przypada dziś ({amount} zł). "
            "Jeśli jeszcze nie zrobiłeś przelewu, wykonaj go jako *instant*."
        ),
    },

    "broadcasts": {
        "normal_payment_changed": (
            "@everyone 🔧 Zmieniono kwotę płatności dla miesięcy zwykłych na **{value} zł**."
        ),
        "holiday_payment_changed": (
            "@everyone 🔧 Zmieniono kwotę płatności dla miesięcy wakacyjnych na **{value} zł**."
        ),
    },

    "confirmations": {
        "normal_payment_updated": (
            "✅ Kwota płatności dla miesięcy zwykłych została zaktualizowana do **{value} zł**."
        ),
        "holiday_payment_updated": (
            "✅ Kwota płatności dla miesięcy wakacyjnych została zaktualizowana do **{value} zł**."
        ),
    },

    "errors": {
        "missing_manager_role": (
            "❌ Nie masz uprawnień do wykonania tej komendy. "
            "Wymagana rola: <@&{role_id}>."
        ),
        "amount_must_be_positive": (
            "❌ Podana kwota musi być większa niż 0."
        ),
        "amount_same_as_current": (
            "❌ Nowa kwota jest taka sama jak obecna ({current} zł)."
        ),
    },

    "system": {
        "config_saved": "✅ Zapisano konfigurację."
    }
}