export type SourceType = 'message' | 'email' | 'photo';

export type AnswerContent = {
	type: AnswerType;
	content: TextContent | MessageContent;
};

export type AnswerType = 'text' | 'message';

export type TextContent = {
	text: string;
};

export type MessageContent = {
	citationId: string;
	messages: Message[];
};

export type Message = {
	speaker: 'other' | 'self';
	text: string;
};

export type Progress = {
	done: boolean;
	text: string;
};
