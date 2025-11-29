import { APP_NAME, APP_VERSION } from '../constants';

const Footer = () => {
  return (
    <footer className="bg-gray-800 text-white py-6">
      <div className="container mx-auto px-4">
        <div className="text-center">
          <p className="text-sm">
            &copy; {new Date().getFullYear()} {APP_NAME}. All rights reserved.
          </p>
          <p className="text-xs text-gray-400 mt-2">Version {APP_VERSION}</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
