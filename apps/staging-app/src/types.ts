export type ActionType = 'create' | 'update' | 'delete';
export type ChangeSource = 'USER' | 'SYSTEM' | 'AUTOMATIC' | 'MANUAL';
export type Status = 'initiated' | 'review' | 'accepted' | 'projected';

export interface StagingChange {
  id: number;
  changeset_id: string;
  record_id: string;
  directory: string;
  action: ActionType;
  market_record_json_new?: Record<string, any>;
  market_record_json_gs?: Record<string, any>;
  change_source: ChangeSource;
  status: Status;
  business_justification?: string;
  revision: number;
  created_by?: string;
  created_at: string;
}