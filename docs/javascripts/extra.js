/* Custom JavaScript for RackSum documentation */

document.addEventListener('DOMContentLoaded', function() {
  // Add copy button functionality to code blocks
  const codeBlocks = document.querySelectorAll('pre code');

  codeBlocks.forEach((block) => {
    // Material theme already handles copy buttons
    // This is a placeholder for any additional custom JS
  });

  // Add smooth scrolling to anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });

  // Add external link indicators
  const links = document.querySelectorAll('.md-content a[href^="http"]');
  links.forEach(link => {
    if (!link.hostname.includes(window.location.hostname)) {
      link.setAttribute('target', '_blank');
      link.setAttribute('rel', 'noopener noreferrer');
    }
  });
});

// Add version warning for older documentation
function checkDocVersion() {
  const currentVersion = document.querySelector('meta[name="version"]');
  if (currentVersion && currentVersion.content !== 'latest') {
    const warning = document.createElement('div');
    warning.className = 'md-banner';
    warning.innerHTML = `
      <div class="md-banner__inner md-grid">
        You are viewing documentation for version ${currentVersion.content}.
        <a href="/">View latest version</a>
      </div>
    `;
    document.body.insertBefore(warning, document.body.firstChild);
  }
}

// Initialize features
checkDocVersion();
