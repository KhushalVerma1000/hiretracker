import { PrismaClient } from "@prisma/client";
let client;
export const db = () => (client ??= new PrismaClient());
