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