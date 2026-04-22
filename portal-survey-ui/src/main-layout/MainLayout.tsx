import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';

interface BreadcrumbItem {
  label: string;
  path?: string;
}

interface MainLayoutProps {
  children: React.ReactNode;
  breadcrumb?: BreadcrumbItem[];
}

const MainLayout: React.FC<MainLayoutProps> = ({ children, breadcrumb }) => {
  const [navCollapsed, setNavCollapsed] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const stored = localStorage.getItem('navCollapsed') === 'true';
    const shouldCollapse = stored || window.innerWidth < 992;
    setNavCollapsed(shouldCollapse);

    const handleResize = () => {
      if (window.innerWidth < 992) {
        setNavCollapsed(true);
      }
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const toggleNav = () => {
    setNavCollapsed((prev) => {
      const next = !prev;
      localStorage.setItem('navCollapsed', String(next));
      return next;
    });
  };

  const isActive = (path: string) => location.pathname === path;

  return (
    <div className={navCollapsed ? 'nav-collapsed' : ''}>
      {/* ==================== ICON BAR ==================== */}
      <aside className="icon-bar">
        <Link to="/" className="brand">VS</Link>
        <ul className="icon-bar-nav">
          <li className="icon-bar-item">
            <Link className={`icon-bar-link${isActive('/') ? ' active' : ''}`} to="/" title="Home">
              <i className="bi bi-house-door"></i>
              <span className="tooltip-text">Home</span>
            </Link>
          </li>
          <li className="icon-bar-item">
            <Link className={`icon-bar-link${isActive('/portfolio') ? ' active' : ''}`} to="/portfolio" title="Portfolio">
              <i className="bi bi-person-badge"></i>
              <span className="tooltip-text">Portfolio</span>
            </Link>
          </li>
          <li className="icon-bar-item">
            <Link className={`icon-bar-link${isActive('/survey') ? ' active' : ''}`} to="/survey" title="Student Survey">
              <i className="bi bi-clipboard-data"></i>
              <span className="tooltip-text">Student Survey</span>
            </Link>
          </li>
          <li className="icon-bar-item">
            <Link className={`icon-bar-link${isActive('/ai-assistant') ? ' active' : ''}`} to="/ai-assistant" title="AI Survey Assistant">
              <i className="bi bi-stars"></i>
              <span className="tooltip-text">AI Survey Assistant</span>
            </Link>
          </li>
          <li className="icon-bar-item">
            <Link className={`icon-bar-link${isActive('/contact') ? ' active' : ''}`} to="/contact" title="Contact">
              <i className="bi bi-envelope"></i>
              <span className="tooltip-text">Contact</span>
            </Link>
          </li>
        </ul>
      </aside>

      {/* ==================== NAVIGATION PANEL ==================== */}
      <aside className="nav-panel" id="navPanel">
        <div className="nav-panel-header">
          <h4>VSTech Solutions</h4>
          <span>Personal Dashboard</span>
        </div>

        <div className="nav-section">
          <div className="nav-section-title">Main Navigation</div>
          <ul className="nav-menu">
            <li className="nav-menu-item">
              <Link className={`nav-menu-link${isActive('/') ? ' active' : ''}`} to="/">
                <i className="bi bi-house-door"></i>
                Home
              </Link>
            </li>
            <li className="nav-menu-item">
              <Link className={`nav-menu-link${isActive('/portfolio') ? ' active' : ''}`} to="/portfolio">
                <i className="bi bi-person-vcard"></i>
                Portfolio
              </Link>
            </li>
            <li className="nav-menu-item">
              <Link className={`nav-menu-link${isActive('/survey') ? ' active' : ''}`} to="/survey">
                <i className="bi bi-ui-checks"></i>
                Student Survey
              </Link>
            </li>
            <li className="nav-menu-item">
              <Link className={`nav-menu-link${isActive('/ai-assistant') ? ' active' : ''}`} to="/ai-assistant">
                <i className="bi bi-stars"></i>
                AI Survey Assistant
              </Link>
            </li>
            <li className="nav-menu-item">
              <Link className={`nav-menu-link${isActive('/contact') ? ' active' : ''}`} to="/contact">
                <i className="bi bi-envelope"></i>
                Contact
              </Link>
            </li>
          </ul>
        </div>

        <div className="nav-section">
          <div className="nav-section-title">Quick Links</div>
          <ul className="nav-menu">
            <li className="nav-menu-item">
              <a
                className="nav-menu-link"
                href="https://github.com/vivek-sarvagod?tab=repositories"
                target="_blank"
                rel="noreferrer"
              >
                <i className="bi bi-github"></i>
                GitHub Profile
              </a>
            </li>
            <li className="nav-menu-item">
              <a
                className="nav-menu-link"
                href="https://linkedin.com/in/vivek-sarvagod"
                target="_blank"
                rel="noreferrer"
              >
                <i className="bi bi-linkedin"></i>
                LinkedIn
              </a>
            </li>
          </ul>
        </div>

        {/* User Info at bottom */}
        <div className="nav-user">
          <div className="nav-user-info">
            <div className="nav-user-avatar">VS</div>
            <div className="nav-user-details">
              <div className="name">Vivek Sarvagod</div>
              <div className="role">Software Architect</div>
            </div>
          </div>
        </div>
      </aside>

      {/* ==================== MAIN WRAPPER ==================== */}
      <div className="main-wrapper">
        {/* Header */}
        <header className="main-header">
          <div className="header-left">
            <button className="menu-toggle" onClick={toggleNav} aria-label="Toggle navigation">
              <i className="bi bi-list"></i>
            </button>
            <nav className="breadcrumb-nav">
              {breadcrumb && breadcrumb.length > 0 ? (
                breadcrumb.map((crumb, idx) => (
                  <React.Fragment key={idx}>
                    {idx > 0 && <span>/</span>}
                    {crumb.path ? (
                      <Link to={crumb.path}>{crumb.label}</Link>
                    ) : (
                      <span className={idx === breadcrumb.length - 1 ? 'current' : ''}>
                        {crumb.label}
                      </span>
                    )}
                  </React.Fragment>
                ))
              ) : (
                <Link to="/">Home</Link>
              )}
            </nav>
          </div>
        </header>

        {/* Main Content */}
        <main className="main-content">{children}</main>
      </div>
    </div>
  );
};

export default MainLayout;
