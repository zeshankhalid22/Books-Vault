import { Link } from "react-router";

export function Header() {
  return (
    <header className="fixed top-0 left-0 w-full bg-blue-400 shadow-md z-10">
      <nav className="container mx-auto p-4">
        <ul className="flex space-x-4">
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to="/contact">Contact</Link>
          </li>
          <li>
            <Link to="/projects">Projects</Link>
          </li>
        </ul>
      </nav>
    </header>
  );
}