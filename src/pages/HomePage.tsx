import { Link } from 'react-router-dom';
import { ROUTES } from '../constants';

const HomePage = () => {
  return (
    <div className="space-y-8">
      <section className="text-center py-12">
        <h1 className="text-5xl font-bold text-gray-800 mb-4">
          Welcome to Car Rental Management System
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Find and rent your perfect car with ease
        </p>
        <Link to={ROUTES.CARS} className="btn-primary inline-block">
          Browse Available Cars
        </Link>
      </section>

      <section className="grid md:grid-cols-3 gap-6">
        <div className="card text-center">
          <div className="text-4xl mb-4">🚗</div>
          <h3 className="text-xl font-semibold mb-2">Wide Selection</h3>
          <p className="text-gray-600">
            Choose from economy to luxury vehicles
          </p>
        </div>
        <div className="card text-center">
          <div className="text-4xl mb-4">💰</div>
          <h3 className="text-xl font-semibold mb-2">Best Prices</h3>
          <p className="text-gray-600">
            Competitive rates and transparent pricing
          </p>
        </div>
        <div className="card text-center">
          <div className="text-4xl mb-4">⭐</div>
          <h3 className="text-xl font-semibold mb-2">Quality Service</h3>
          <p className="text-gray-600">
            24/7 customer support and assistance
          </p>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
