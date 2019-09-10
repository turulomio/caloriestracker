
export type UserType = {
    id: string;
    name: string;
}

export type Query={
    nodes: UserType[];
}