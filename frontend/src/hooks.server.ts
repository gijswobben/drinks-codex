import { GITHUB_ID, GITHUB_SECRET } from "$env/static/private";
import { loginUsernamePassword, getCurrentUserInfo, swapGithubToken } from "$lib/functions";
import Credentials from "@auth/core/providers/credentials";
import GitHub from "@auth/core/providers/github";
import type { User as AuthUser } from "@auth/core/types";
import { SvelteKitAuth } from "@auth/sveltekit";

export const handle = SvelteKitAuth({
    theme: {
        brandColor: "#FF6600",
    },

    providers: [

        // Username and password login
        Credentials({

            // Define the fields of the login form
            credentials: {
                username: { label: "Username", type: "text", placeholder: "Email" },
                password: { label: "Password", type: "password", placeholder: "Password" }
            },

            // Authorize the user with the form data
            async authorize(credentials, request): Promise<AuthUser | null> {

                // Extract the credentials
                const username = credentials.username as string;
                const password = credentials.password as string;

                // Fetch the token for this user
                const token = await loginUsernamePassword({ username, password })

                // Use the token to fetch the user
                const user = await getCurrentUserInfo({ token: token });

                return {
                    id: user.email,
                    name: user.full_name,
                    email: user.email,
                    image: user.profile_picture_url,
                    access_token: token.access_token,  // Store the token on the user object
                } as AuthUser;
            },
        }),

        // GitHub OAuth login
        GitHub({
            clientId: GITHUB_ID,
            clientSecret: GITHUB_SECRET,
        }),
    ],

    // Define the callbacks
    callbacks: {

        // Called when the user is successfully authenticated to create a JWT
        async jwt({ token, account, user }) {

            // If the provider was Github, swap the access_token for a JWT from our backend
            if (account && account.provider === "github") {
                token.access_token = (await swapGithubToken({ github_access_token: account?.access_token as string })).access_token;

                // If the provider was credentials, store the access_token from the user object
            } else if (account && account.provider === "credentials") {
                token.access_token = user.access_token;
            }
            return token;
        },
        async session({ session, token }) {

            // Get and store the user data on the session
            session.user = await getCurrentUserInfo({ token: token.access_token as string });

            // Set the access_token for use in subsequent API requests
            session.access_token = token.access_token

            return session
        }
    },

});
