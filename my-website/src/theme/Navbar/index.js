import React from 'react';
import Navbar from '@theme-original/Navbar';
import { useLocation } from '@docusaurus/router';

// Custom Navbar component with mobile improvements
export default function NavbarWrapper(props) {
  const location = useLocation();

  // Add mobile-specific enhancements
  React.useEffect(() => {
    // Add mobile-specific behavior if needed
    const handleResize = () => {
      const isMobile = window.innerWidth < 996; // Docusaurus mobile breakpoint
      if (isMobile) {
        // Add mobile-specific classes or behavior
        document.body.classList.add('mobile-navbar');
      } else {
        document.body.classList.remove('mobile-navbar');
      }
    };

    // Initial check
    handleResize();

    // Add resize listener
    window.addEventListener('resize', handleResize);

    // Cleanup
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <>
      <Navbar {...props} />
      {/* Additional mobile-specific UI elements can be added here */}
    </>
  );
}