import React, { useEffect, useState, ReactElement } from 'react';
import CircularProgress from '@material-ui/core/CircularProgress';

type Props = {
  children: ReactElement;
  loadingFunction: () => Promise<void>; //Currently no error handling
};

const Loading: React.FC<Props> = (props: Props) => {
  const { children, loadingFunction } = props;
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    if (loaded) return;
    loadingFunction().then(() => setLoaded(true));
  }, [loaded, loadingFunction]);

  if (loaded) {
    return children;
  } else {
    return <CircularProgress />;
  }
};

export default Loading;
