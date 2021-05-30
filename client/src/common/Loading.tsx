import React, { useEffect, useState, ReactElement } from 'react';
import CircularProgress from '@material-ui/core/CircularProgress';

type Props = {
  children: ReactElement;
  loadingFunction: () => Promise<string | void>;
};

// todo: retry button
const Loading: React.FC<Props> = (props: Props) => {
  const { children, loadingFunction } = props;
  const [loaded, setLoaded] = useState<boolean>(false);
  const [error, setError] = useState<string | undefined>(undefined);

  useEffect(() => {
    if (loaded || error) return;
    loadingFunction()
      .then(() => setLoaded(true))
      .catch((errorMessage) => setError(errorMessage));
  }, [loaded, setLoaded, loadingFunction, error, setError]);

  if (loaded) {
    return children;
  } else if (error) {
    return <div>{error}</div>;
  } else {
    return <CircularProgress />;
  }
};

export default Loading;
