{{/*
Expand the name of the chart.
*/}}
{{- define "redis-docs.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "redis-docs.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "redis-docs.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels.
*/}}
{{- define "redis-docs.labels" -}}
helm.sh/chart: {{ include "redis-docs.chart" . }}
{{ include "redis-docs.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels.
*/}}
{{- define "redis-docs.selectorLabels" -}}
app.kubernetes.io/name: {{ include "redis-docs.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use.
*/}}
{{- define "redis-docs.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "redis-docs.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Return the image reference for the main container.
Priority: global.registry > image.registry
*/}}
{{- define "redis-docs.image" -}}
{{- $registry := .Values.global.registry | default .Values.image.registry -}}
{{- printf "%s/%s:%s" $registry .Values.image.name (.Values.image.tag | default .Chart.AppVersion) -}}
{{- end }}

{{/*
Return the TLS secret name.
*/}}
{{- define "redis-docs.tlsSecretName" -}}
{{- if .Values.tls.existingSecret -}}
{{- .Values.tls.existingSecret -}}
{{- else -}}
{{- printf "%s-tls" (include "redis-docs.fullname" .) -}}
{{- end -}}
{{- end }}

{{/*
Return the image reference for the metrics sidecar.
Priority: global.registry > metrics.image.registry
*/}}
{{- define "redis-docs.metricsImage" -}}
{{- $registry := .Values.global.registry | default .Values.metrics.image.registry -}}
{{- printf "%s/%s:%s" $registry .Values.metrics.image.name .Values.metrics.image.tag -}}
{{- end }}

{{/*
Return the image reference for the CLI proxy container.
Priority: global.registry > cli.image.registry
*/}}
{{- define "redis-docs.cliImage" -}}
{{- $registry := .Values.global.registry | default .Values.cli.image.registry -}}
{{- printf "%s/%s:%s" $registry .Values.cli.image.name .Values.cli.image.tag -}}
{{- end }}

{{/*
Return the image reference for the CLI Redis sidecar.
Priority: global.registry > cli.redis.image.registry
*/}}
{{- define "redis-docs.cliRedisImage" -}}
{{- $registry := .Values.global.registry | default .Values.cli.redis.image.registry -}}
{{- printf "%s/%s:%s" $registry .Values.cli.redis.image.name .Values.cli.redis.image.tag -}}
{{- end }}

{{/*
Return the image reference for the search API container. It is the CLI proxy
image: the search service ships inside it rather than in one of its own.
Priority: global.registry > search.image.registry
*/}}
{{- define "redis-docs.searchImage" -}}
{{- $registry := .Values.global.registry | default .Values.search.image.registry -}}
{{- printf "%s/%s:%s" $registry .Values.search.image.name .Values.search.image.tag -}}
{{- end }}

{{/*
Return the image reference for the search index's Redis.
Priority: global.registry > search.redis.image.registry
*/}}
{{- define "redis-docs.searchRedisImage" -}}
{{- $registry := .Values.global.registry | default .Values.search.redis.image.registry -}}
{{- printf "%s/%s:%s" $registry .Values.search.redis.image.name .Values.search.redis.image.tag -}}
{{- end }}

{{/*
Return the image reference for the Jupyter sidecar.
Priority: global.registry > cli.jupyter.image.registry
*/}}
{{- define "redis-docs.cliJupyterImage" -}}
{{- $registry := .Values.global.registry | default .Values.cli.jupyter.image.registry -}}
{{- printf "%s/%s:%s" $registry .Values.cli.jupyter.image.name .Values.cli.jupyter.image.tag -}}
{{- end }}

{{/*
Sanitize PEM certificate text by stripping Windows carriage returns.
*/}}
{{- define "redis-docs.cleanPem" -}}
{{- . | replace "\r" "" -}}
{{- end }}

{{/*
Whether the download widget has bundles to offer: "true" or "".

Packing writes this deployment's base URL into every archive, so it needs a
canonical URL fixed at install time. Without one the site resolves its base URL
per request from the Host header, which no file on disk can carry — so the
bundles cannot be built and the widget is hidden rather than left to 404.
*/}}
{{- define "redis-docs.downloadsActive" -}}
{{- if and .Values.downloads.enabled .Values.canonicalURL -}}true{{- end -}}
{{- end }}

{{/*
Whether a catalog link's url is a path on this site rather than another host.
A protocol-relative `//host/...` starts with a slash too, and is not.
*/}}
{{- define "redis-docs.isSiteLink" -}}
{{- $url := . | default "" | toString -}}
{{- if and (hasPrefix "/" $url) (not (hasPrefix "//" $url)) -}}true{{- end -}}
{{- end }}

{{/*
Return the image reference for the mirrored sections.
Priority: global.registry > mirror.image.registry
*/}}
{{- define "redis-docs.mirrorImage" -}}
{{- $registry := .Values.global.registry | default .Values.mirror.image.registry -}}
{{- printf "%s/%s:%s" $registry .Values.mirror.image.name .Values.mirror.image.tag -}}
{{- end }}

{{/*
The paths the mirror serves, as nginx location prefixes. Named once here
because three templates need the same list: the proxy rules, the runtime
config that unlinks them when the mirror is not deployed, and the README.
*/}}
{{- define "redis-docs.mirrorPaths" -}}
blog tutorials compare solutions customers technology resources/architecture-diagrams images/site-mirror
{{- end }}
