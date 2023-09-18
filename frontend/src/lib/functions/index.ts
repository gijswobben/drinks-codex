import { BACKEND_BASE_URL } from "$lib/config";
import type { Token, User } from "$lib/types";

export async function callApi<T>({ url, token, method = "GET", body, headers }: { url: string, token?: Token | string, method?: string, body?: string, headers?: HeadersInit }): Promise<T> {

    // Check if the URL starts with a slash
    if (!url.startsWith("/")) {
        url = "/" + url;
    }

    // Construct the headers
    let combinedHeaders: HeadersInit = {
        "Content-Type": "application/json",
    }
    if (token !== undefined) {
        if (typeof token === "string") {
            combinedHeaders["Authorization"] = token;
        } else {
            combinedHeaders["Authorization"] = token.access_token as string;
        }
    }
    if (headers) {
        combinedHeaders = { ...combinedHeaders, ...headers }
    }

    // Make the request
    const response = await fetch(`${BACKEND_BASE_URL}${url}`, {
        method: method,
        headers: combinedHeaders,
        body: body,
    });

    // Check if the response is OK
    if (!response.ok) {
        throw new Error(response.statusText);
    }

    // Return the response
    return await response.json() as T;
}

export async function loginUsernamePassword({ username, password }: { username: string, password: string }): Promise<Token> {
    return await callApi<Token>({
        url: "/v1/api/auth/token",
        method: "POST",
        body: new URLSearchParams({ username, password }).toString(),
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        }
    });
}

export async function getCurrentUserInfo({ token }: { token: Token | string }): Promise<User> {
    return await callApi<User>({
        url: "/v1/api/users/me",
        token: typeof token === "string" ? token : token.access_token,
    });
}

export async function swapGithubToken({ github_access_token }: { github_access_token: string }): Promise<Token> {
    return await callApi<Token>({
        url: `/v1/api/auth/github-token?github_access_token=${github_access_token}`,
        method: "POST",
    });
}