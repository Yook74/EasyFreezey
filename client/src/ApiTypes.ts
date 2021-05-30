export type Session = {
  id: number;
  date: string;
};

const parseSession = (json: any): Session => {
  if (!(json && Number.isInteger(json.id) && typeof json.date === 'string')) {
    throw new TypeError();
  }

  return { id: json.id, date: json.date };
};

export const parseSessionListResponse = (json: any): Session[] => {
  if (!(json && Array.isArray(json))) {
    throw new TypeError();
  }

  return json.map((session) => parseSession(session));
};
