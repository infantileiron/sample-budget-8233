import {request} from "./client";export const fetchDraws=()=>request("/draws");export const createDraws=(body:unknown)=>request("/draws","POST",body);
