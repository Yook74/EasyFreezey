export type Session = {
  id?: number;
  date: string;
  recipientNames?: string[];
};

const parseSession = (json: any): Session => {
  if (!(json && Number.isInteger(json.id) && typeof json.date === 'string')) {
    throw new TypeError();
  }

  const session: Session = { date: json.date };
  if (Number.isInteger(json.id)) {
    session.id = json.id;
  }
  if (Array.isArray(json.recipient_names)) {
    session.recipientNames = json.recipient_names.map((name: any) => {
      if (typeof name !== 'string') {
        throw new TypeError();
      }
      return name;
    });
  }

  return session;
};

export const parseSessionList = (json: any): Session[] => {
  if (!(json && Array.isArray(json))) {
    throw new TypeError();
  }

  return json.map((session) => parseSession(session));
};
