/* ------------------------------ Burger Menu Mobile Nav -------------------------------- */
/* -------------------------------------------------------------------------------------- */
// Get the menu elements
const menuButton = document.querySelector('[aria-label="Global"] button');
const mobileMenu = document.querySelector('[role="dialog"]');

// Set initial state - hide menu on page load
if (mobileMenu) {
  mobileMenu.style.display = 'none';
}

// Only proceed if we have the necessary elements
if (menuButton && mobileMenu) {
  // Use a more specific selector for the close button
  const closeButton = mobileMenu.querySelector('button[aria-label="Close menu"]');
  const backdrop = mobileMenu.querySelector('.fixed.inset-0');
  const menuContent = mobileMenu.querySelector('.mt-6.flow-root');

  // Function to open the menu
  const openMenu = () => {
    mobileMenu.style.display = 'block';
    mobileMenu.classList.remove('lg:hidden');
    if (backdrop) {
      backdrop.classList.add('bg-gray-900/80');
    }
    if (menuContent) {
      menuContent.classList.remove('hidden');
    }
    document.body.style.overflow = 'hidden';
  };

  // Function to close the menu
  const closeMenu = () => {
    mobileMenu.style.display = 'none';
    mobileMenu.classList.add('lg:hidden');
    if (backdrop) {
      backdrop.classList.remove('bg-gray-900/80');
    }
    if (menuContent) {
      menuContent.classList.add('hidden');
    }
    document.body.style.overflow = '';
  };

  // Add click event listener to menu button
  menuButton.addEventListener('click', (e) => {
    e.preventDefault();
    openMenu();
  });

  // Add click event listener to close button if it exists
  if (closeButton) {
    closeButton.addEventListener('click', (e) => {
      e.preventDefault();
      closeMenu();
    });
  }

  // Add click event listener to backdrop if it exists
  if (backdrop) {
    backdrop.addEventListener('click', (event) => {
      if (event.target === backdrop) {
        closeMenu();
      }
    });
  }

  // Add escape key listener
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      closeMenu();
    }
  });

  // Hide menu initially
  closeMenu();
}

/* ------------------------------ Controller for Modals --------------------------------- */
/* -------------------------------------------------------------------------------------- */
class ModalController {
    constructor() {
        this.init();
        this.setupHtmxListeners();
    }

    init() {
        // Handle close buttons
        document.addEventListener('click', (e) => {
            if (e.target.hasAttribute('data-dialog-close')) {
                this.closeModal();
            }
        });

        // Handle backdrop close
        document.addEventListener('click', (e) => {
            if (e.target.hasAttribute('data-dialog-backdrop') &&
                e.target.hasAttribute('data-dialog-backdrop-close')) {
                this.closeModal();
            }
        });

        // Handle Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeModal();
            }
        });
    }

    setupHtmxListeners() {
        // Listen for HTMX before request
        document.addEventListener('htmx:beforeRequest', (evt) => {
            const trigger = evt.detail.elt;
            if (trigger.hasAttribute('data-dialog-target')) {
                this.openModal();
            }
        });

        // Listen for HTMX after request
        document.addEventListener('htmx:afterRequest', (evt) => {
            const trigger = evt.detail.elt;
            const targetElement = document.querySelector('#project-tasks');

            // If this was a form submission
            if (trigger.tagName === 'FORM') {
                // Only close modal on successful submission (status 2xx)
                if (evt.detail.successful && evt.detail.xhr.status < 300) {
                    // Check if the response indicates success (tasks list returned)
                    if (evt.detail.target && evt.detail.target.id === 'project-tasks') {
                        setTimeout(() => {
                            this.closeModal();
                        }, 300);
                    }
                }
                // Keep modal open for errors
                else if (evt.detail.xhr.status >= 400) {
                    this.openModal(); // Ensure modal stays open
                }
            }
            // If this was opening the modal
            else if (trigger.hasAttribute('data-dialog-target')) {
                if (evt.detail.successful) {
                    this.openModal();
                }
            }
        });

        // Handle form errors in beforeSwap
        document.addEventListener('htmx:beforeSwap', (evt) => {
            const trigger = evt.detail.elt;

            // If the response status is an error (4xx or 5xx)
            if (evt.detail.xhr.status >= 400) {
                evt.detail.shouldSwap = true; // Ensure the error content is swapped
                evt.detail.isError = false;   // Prevent HTMX from treating it as an error

                // If this is a form submission, ensure the modal stays open
                if (trigger.tagName === 'FORM') {
                    setTimeout(() => {
                        this.openModal();
                    }, 0);
                }
            }
        });
    }

    openModal() {
        const backdrop = document.querySelector('[data-dialog-backdrop]');
        if (backdrop) {
            backdrop.classList.remove('pointer-events-none', 'opacity-0');

            const dialog = backdrop.querySelector('[data-dialog]');
            if (dialog) {
                dialog.classList.remove('opacity-0', '-translate-y-14');
                dialog.classList.add('opacity-1', 'translate-y-0');

                setTimeout(() => {
                    const firstInput = dialog.querySelector('input:not([type="hidden"]), select, textarea');
                    if (firstInput) {
                        firstInput.focus();
                    }
                }, 100);
            }
        }
    }

    closeModal() {
        const backdrop = document.querySelector('[data-dialog-backdrop]');
        if (backdrop) {
            const dialog = backdrop.querySelector('[data-dialog]');
            if (dialog) {
                dialog.classList.remove('opacity-1', 'translate-y-0');
                dialog.classList.add('opacity-0', '-translate-y-14');

                setTimeout(() => {
                    backdrop.classList.add('pointer-events-none', 'opacity-0');
                }, 300);
            }
        }
    }
}

// Initialize the modal controller
document.addEventListener('DOMContentLoaded', () => {
    window.modalController = new ModalController();
});
