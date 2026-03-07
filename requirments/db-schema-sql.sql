-- WARNING: This schema is for context only and is not meant to be run.
-- Table order and constraints may not be valid for execution.

CREATE TABLE public.snaap_pods (
  pod_id uuid NOT NULL DEFAULT uuid_generate_v4(),
  pod_created_at timestamp with time zone NOT NULL DEFAULT now(),
  pod_name character varying,
  pod_description text,
  pod_configuration character varying,
  pod_current_status character varying,
  pod_current_location character varying NOT NULL,
  rbn_id uuid,
  CONSTRAINT snaap_pods_pkey PRIMARY KEY (pod_id),
  CONSTRAINT snaap_pods_rbn_id_fkey FOREIGN KEY (rbn_id) REFERENCES public.snaap_ribbonways(rbn_id)
);
CREATE TABLE public.snaap_portal_docks (
  dck_id uuid NOT NULL DEFAULT uuid_generate_v4(),
  dck_created_at timestamp with time zone NOT NULL DEFAULT now(),
  dck_name character varying,
  dck_description text,
  dck_geofence_location json,
  ptl_id uuid NOT NULL,
  CONSTRAINT snaap_portal_docks_pkey PRIMARY KEY (dck_id),
  CONSTRAINT snaap_portal_docks_ptl_id_fkey FOREIGN KEY (ptl_id) REFERENCES public.snaap_ribbonway_portals(ptl_id)
);
CREATE TABLE public.snaap_ribbonway_portals (
  ptl_id uuid NOT NULL DEFAULT uuid_generate_v4(),
  ptl_created_at timestamp with time zone NOT NULL DEFAULT now(),
  ptl_name character varying,
  ptl_description text,
  ptl_geofence_location json,
  rbn_id uuid,
  CONSTRAINT snaap_ribbonway_portals_pkey PRIMARY KEY (ptl_id),
  CONSTRAINT snaap_ribbonway_portals_rbn_id_fkey FOREIGN KEY (rbn_id) REFERENCES public.snaap_ribbonways(rbn_id)
);
CREATE TABLE public.snaap_ribbonways (
  rbn_id uuid NOT NULL DEFAULT uuid_generate_v4(),
  rbn_created_at timestamp with time zone NOT NULL DEFAULT now(),
  rbn_name character varying,
  rbn_description text,
  rbn_geofence_location json,
  CONSTRAINT snaap_ribbonways_pkey PRIMARY KEY (rbn_id)
);
CREATE TABLE public.snaap_ride_requests (
  rde_id uuid NOT NULL DEFAULT uuid_generate_v4(),
  rde_created_at timestamp with time zone NOT NULL DEFAULT now(),
  rde_boarding_time timestamp with time zone,
  rde_dropoff_time timestamp with time zone,
  rde_amount_charged numeric,
  rde_currency_charged character varying,
  rdr_id uuid,
  ptl_id uuid,
  pod_id uuid,
  rde_starting_dock uuid DEFAULT gen_random_uuid(),
  rde_ending_dock uuid DEFAULT gen_random_uuid(),
  CONSTRAINT snaap_ride_requests_pod_id_fkey FOREIGN KEY (pod_id) REFERENCES public.snaap_pods(pod_id),
  CONSTRAINT snaap_ride_requests_ptl_id_fkey FOREIGN KEY (ptl_id) REFERENCES public.snaap_ribbonway_portals(ptl_id),
  CONSTRAINT snaap_ride_requests_rdr_id_fkey FOREIGN KEY (rdr_id) REFERENCES public.snaap_riders(rdr_id)
);
CREATE TABLE public.snaap_riders (
  rdr_id uuid NOT NULL DEFAULT uuid_generate_v4(),
  rdr_created_at timestamp with time zone NOT NULL DEFAULT now(),
  rdr_first_name character varying,
  rdr_last_name character varying,
  rdr_email character varying,
  rdr_phone_number character varying,
  rdr_password character varying,
  rdr_avatar character varying,
  CONSTRAINT snaap_riders_pkey PRIMARY KEY (rdr_id)
);