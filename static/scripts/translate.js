const translations = {
    en: {
        search: 'Search',
        home: 'Home',
        logout: 'Log out',
        imageLens: 'Image Lens',
        costs: 'Pricing',
        contact: 'Contact',
        login: 'Login',
        register: 'Register',
        searchPlaceholder: 'Search...',
        imageLensTitle: 'Image Lens',
        imageLensDescription: 'Upload an image for advanced search'
    },
    de: {
        search: 'Suchen',
        home: 'Startseite',
        logout: 'Abmelden',
        imageLens: 'Bild-Suche',
        costs: 'Kosten',
        contact: 'Kontakt',
        login: 'Anmelden',
        register: 'Registrieren',
        searchPlaceholder: 'Suchen...',
        imageLensTitle: 'Bild-Suche',
        imageLensDescription: 'Laden Sie ein Bild für die erweiterte Suche hoch'
    }
};

// Language Change Handler
function changeLanguage(lang) {
    // Update Navigation Links
    document.querySelectorAll('[data-lang-key]').forEach(element => {
        const key = element.getAttribute('data-lang-key');
        element.textContent = translations[lang][key];
    });

    // Update Search Input Placeholder
    const searchInput = document.querySelector('.search-input');
    if (searchInput) {
        searchInput.placeholder = translations[lang].searchPlaceholder;
    }

    // Update Image Lens Content
    const imageLensTitle = document.querySelector('.image-lens-container h2');
    const imageLensDescription = document.querySelector('.image-lens-container p');
    if (imageLensTitle && imageLensDescription) {
        imageLensTitle.textContent = translations[lang].imageLensTitle;
        imageLensDescription.textContent = translations[lang].imageLensDescription;
    }

    // Optional: Store language preference
    localStorage.setItem('selectedLanguage', lang);
}

// Language Selector Event Listener
document.getElementById('languageSelector').addEventListener('change', function(e) {
    changeLanguage(e.target.value);
});

// Check for Stored Language Preference
document.addEventListener('DOMContentLoaded', () => {
    const storedLang = localStorage.getItem('selectedLanguage') || 'en';
    document.getElementById('languageSelector').value = storedLang;
    changeLanguage(storedLang);
});