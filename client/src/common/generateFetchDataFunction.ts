const generateFetchDataFunction = (
  urlToGet: string,
  onSuccess: (json: any) => void,
  errorMessage: string
) => {
  return () => {
    return new Promise<string | void>((resolve, reject) => {
      fetch(urlToGet)
        .then((response) => {
          return response.json();
        })
        .then((json: any) => {
          try {
            onSuccess(json);
            resolve();
          } catch (e) {
            return Promise.reject();
          }
        })
        .catch((error: Error) => {
          reject(errorMessage);
        });
    });
  };
};

export default generateFetchDataFunction;
