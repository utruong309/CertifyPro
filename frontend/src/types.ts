export interface User {
    id?: number;
    name: string;
    email: string;
    role: string;
    department?: string;
  }
  
  export interface Certification {
    id?: number;
    type: string;
    number: string;
    issue_date: string;
    expiry_date: string;
    state: string;
    user_id: number;
    status?: string;
    document_path?: string | null;
  }
  
  export interface Stats {
    total: number;
    active: number;
    expiring_soon: number;
    expired: number;
  }  