import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export async function proxy(request: NextRequest) {
  const token = request.cookies.get('token')?.value;

  // Handle Proxying
  if (request.nextUrl.pathname.startsWith('/api/proxy/')) {
    const requestHeaders = new Headers(request.headers);
    if (token) {
      requestHeaders.set('Authorization', `Bearer ${token}`);
    }
    
    // Remove Next.js proxy prefix and point to backend
    const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
    const destination = request.nextUrl.pathname.replace('/api/proxy/', '/');
    
    return NextResponse.rewrite(new URL(`${backendUrl}${destination}${request.nextUrl.search}`), {
      request: {
        headers: requestHeaders,
      }
    });
  }

  // Handle Auth Protection
  const protectedPaths = ['/grade', '/history'];
  const isProtectedPath = protectedPaths.some(path => request.nextUrl.pathname.startsWith(path));

  const authPaths = ['/login', '/register'];
  const isAuthPath = authPaths.some(path => request.nextUrl.pathname.startsWith(path));

  if (isProtectedPath && !token) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  if (isAuthPath && token) {
    return NextResponse.redirect(new URL('/grade', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico).*)'], // Removed api ignore so it hits proxy
};
