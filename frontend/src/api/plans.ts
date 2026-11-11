import {request} from "./client";export const fetchPlans=()=>request("/plans");export const createPlans=(body:unknown)=>request("/plans","POST",body);
