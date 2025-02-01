import { render, screen } from '@/lib/test-utils';
import { LoadingDots } from '../loading-dots';

describe('LoadingDots', () => {
  it('renders with default styles', () => {
    render(<LoadingDots />);
    const container = screen.getAllByRole('presentation')[0];
    expect(container).toBeInTheDocument();
    expect(container).toHaveClass('flex', 'space-x-1');
  });

  it('applies custom className', () => {
    render(<LoadingDots className="test-class" />);
    const container = screen.getAllByRole('presentation')[0];
    expect(container).toHaveClass('test-class');
  });

  it('renders three dots', () => {
    render(<LoadingDots />);
    const dots = screen.getAllByRole('presentation');
    expect(dots).toHaveLength(4); // 1 container + 3 dots
  });
}); 