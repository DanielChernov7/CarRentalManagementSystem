import { Link } from 'react-router-dom';
import { ROUTES, APP_NAME } from '../constants';

const Header = () => {
  return (
    <header className="bg-blue-600 text-white shadow-lg">
      <nav className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to={ROUTES.HOME} className="text-2xl font-bold">
            {APP_NAME}
          </Link>
          <ul className="flex space-x-6">
            <li>
              <Link to={ROUTES.HOME} className="hover:text-blue-200 transition-colors">
                Home
              </Link>
            </li>
            <li>
              <Link to={ROUTES.CARS} className="hover:text-blue-200 transition-colors">
                Cars
              </Link>
            </li>
            <li>
              <Link to={ROUTES.RENTALS} className="hover:text-blue-200 transition-colors">
                Rentals
              </Link>
            </li>
            <li>
              <Link to={ROUTES.LOGIN} className="hover:text-blue-200 transition-colors">
                Login
              </Link>
            </li>
          </ul>
        </div>
      </nav>
    </header>
  );
};

export default Header;
