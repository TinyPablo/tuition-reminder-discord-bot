MESSAGES_PL = {
    "reminders": {
        "week_before_due": (
            "@everyone {date} 📅 Przypomnienie — jeśli jeszcze nie zrobiłeś/aś przelewu ({amount} zł), ogarnij to w wolnej chwili."
        ),
        "day_before_due": (
            "@everyone {date} ⚠️ Przypomnienie — jeśli jeszcze nie zapłaciłeś/aś czesnego ({amount} zł), możesz to zrobić dziś zwykłym przelewem bez dodatkowych kosztów."
        ),
        "due_today": (
            "@everyone {date} 🚨 Przypomnienie — jeżeli jeszcze nie przelałeś/aś, to przelewaj kasę teraz przelewem natychmiastowym ({amount} zł), bo dziś termin. Jak to odłożysz, możesz mieć potem problemy."
        ),
    },

    "broadcasts": {
        "normal_payment_changed": (
            "@everyone ℹ️ Info — czesne za zwykłe miesiące zmienione na **{value} zł**."
        ),
        "holiday_payment_changed": (
            "@everyone ℹ️ Info — czesne za wakacyjne miesiące zmienione na **{value} zł**."
        ),
    },

    "confirmations": {
        "normal_payment_updated": (
            "✅ Aktualizacja — kwota na zwykłe miesiące ustawiona na **{value} zł**."
        ),
        "holiday_payment_updated": (
            "✅ Aktualizacja — kwota na wakacyjne miesiące ustawiona na **{value} zł**."
        ),
    },

    "errors": {
        "missing_manager_role": "❌ Błąd — nie masz uprawnień do tej komendy. Wymagana rola: <@&{role_id}>.",
        "amount_must_be_positive": "❌ Błąd — kwota musi być większa niż 0.",
        "amount_same_as_current": "❌ Błąd — nowa kwota jest taka sama jak obecna ({current} zł).",
    },

    "system": {
        "config_saved": "✅ Konfiguracja zapisana — gotowe."
    }
}