import {request} from "./client";export const fetchLots=()=>request("/lots");export const createLots=(body:unknown)=>request("/lots","POST",body);
