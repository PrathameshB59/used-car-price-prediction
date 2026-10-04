/*
 * AutoValue AI
 * ============================================================
 * Theme initialization and persistence.
 *
 * WHY:
 * Theme handling must happen before the main application loads
 * so users do not see a flash of the wrong theme.
 *
 * INPUT:
 * localStorage preference or browser system preference.
 *
 * OUTPUT:
 * <html data-theme="light|dark">
 */

(function initializeTheme() {
    const STORAGE_KEY = "autovalue-theme";
    const root = document.documentElement;

    /*
     * Purpose:
     * Read the user's saved theme.
     *
     * Returns:
     * "light", "dark", or null.
     */
    function getSavedTheme() {
        try {
            return localStorage.getItem(STORAGE_KEY);
        } catch {
            return null;
        }
    }

    /*
     * Purpose:
     * Detect the operating system/browser preference.
     *
     * Returns:
     * "light" or "dark".
     */
    function getSystemTheme() {
        if (
            window.matchMedia &&
            window.matchMedia("(prefers-color-scheme: light)").matches
        ) {
            return "light";
        }

        return "dark";
    }

    const savedTheme = getSavedTheme();
    const theme = savedTheme || getSystemTheme();

    root.setAttribute("data-theme", theme);

    /*
     * Expose a tiny public API for the header toggle.
     *
     * WHY:
     * Other frontend modules can change the theme without
     * duplicating localStorage logic.
     */
    window.AutoValueTheme = {
        get() {
            return root.getAttribute("data-theme") || "dark";
        },

        set(nextTheme) {
            const safeTheme =
                nextTheme === "light"
                    ? "light"
                    : "dark";

            root.setAttribute("data-theme", safeTheme);

            try {
                localStorage.setItem(
                    STORAGE_KEY,
                    safeTheme
                );
            } catch {
                // Theme still works even if storage is unavailable.
            }
        },

        toggle() {
            const current = this.get();

            this.set(
                current === "dark"
                    ? "light"
                    : "dark"
            );
        }
    };
})();
