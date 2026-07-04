-- Blue Life Commons media storage registry.
-- This schema is the operational database layer for object storage metadata.
-- Git remains the transparent export/review layer; this database is for
-- workflow, search, grants, variants, and audit history.

create table if not exists media_source (
  id bigserial primary key,
  source_url text not null unique,
  source_host text,
  source_type text,
  title text,
  retrieved_at timestamptz,
  created_at timestamptz not null default now()
);

create table if not exists media_rights_grant (
  id bigserial primary key,
  grant_key text not null unique,
  rights_status text not null,
  license text,
  license_url text,
  creator text,
  credit text,
  granted_by text,
  allowed_surfaces text[] not null default '{}',
  blocked_surfaces text[] not null default '{}',
  expires_at timestamptz,
  notes text,
  created_at timestamptz not null default now()
);

create table if not exists media_asset (
  id bigserial primary key,
  artifact_id text not null,
  species_page text not null,
  taxon_group text not null,
  slug text not null,
  common_name text not null,
  scientific_name text,
  approved_asset_id text not null unique,
  source_id bigint references media_source(id),
  rights_grant_id bigint references media_rights_grant(id),
  storage_provider text not null default 'cloudflare_r2',
  bucket text not null,
  object_prefix text not null unique,
  source_object_key text,
  source_checksum_sha256 text,
  source_ext text,
  status text not null default 'mirror_pending',
  approved_at timestamptz,
  mirrored_at timestamptz,
  retired_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists media_variant (
  id bigserial primary key,
  media_asset_id bigint not null references media_asset(id) on delete cascade,
  variant_name text not null,
  role text not null,
  object_key text not null unique,
  public_url text,
  public_use boolean not null default false,
  format text not null,
  width integer,
  height integer,
  bytes bigint,
  checksum_sha256 text,
  status text not null default 'pending_generation',
  generated_at timestamptz,
  created_at timestamptz not null default now(),
  unique (media_asset_id, variant_name)
);

create table if not exists media_review_event (
  id bigserial primary key,
  artifact_id text not null,
  approved_asset_id text,
  event_type text not null,
  reviewer text,
  decision text,
  notes text,
  evidence jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create index if not exists media_asset_artifact_id_idx on media_asset (artifact_id);
create index if not exists media_asset_status_idx on media_asset (status);
create index if not exists media_variant_public_use_idx on media_variant (public_use);
create index if not exists media_review_event_artifact_id_idx on media_review_event (artifact_id);
