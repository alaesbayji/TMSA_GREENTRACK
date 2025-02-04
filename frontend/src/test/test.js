import { render, screen } from '@testing-library/react';
import MapComponent from './MapComponent';

test('renders map component', () => {
  render(<MapComponent />);
  expect(screen.getByText(/Test popup/i)).toBeInTheDocument();
});
