export interface Institution {
  id: number;
  name: string;
  slug: string;
  logo_path?: string;
  branding_colors: string[];
  tagline?: string;
}

export interface IdentityPayload {
  external_id: string;
  first_name: string;
  last_name: string;
  email?: string;
  role?: string;
  department?: string;
  institution_id: number;
}

