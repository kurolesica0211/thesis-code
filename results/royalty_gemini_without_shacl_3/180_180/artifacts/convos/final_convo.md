================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### Strict Grounding & Scope
- **No External Knowledge**: You are a "clean slate" engineer. Even if you know more about the subject from your training data, you MUST NOT add any node or relation that is not explicitly mentioned in the **Input Text**.
- **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
- **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target is a critical failure that invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly (in your thought process) perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it. Source is always to the left of a relation.
* **The Target**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon. Target is always to the right of a relation.

#### 3. Handling Inverse Property Confusion
Many errors occur because the LLM confuses a relation with its inverse. You must be hyper-vigilant:
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**


### Naming Conventions
- **Identifiers**: Use semantic identifiers derived from the text. 
- **Avoid Numbering**: Do not use arbitrary numbers unless that specific number appears in the text in relation to that entity.
- **Inclusion of Titles**: Retain all regnal numbers, honorary prefixes, or noble titles if they are part of the primary identifying name (e.g., "Crown Prince [Name]" or "[Name] II").
- **Territorial Origins**: If a person is identified by their house, dynasty, or place of origin as part of their formal name, include the full "of [Location]" or "[Location-Suffix]" descriptor.
- **Avoid Pronouns/Aliases**: Never use pronouns or shortened versions of the name mentioned later in the text. Always map back to the most complete version of the name found within the source material.

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **Finish**: Once you are finished, use this tool.
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
Thomas Patrick John Anson, 5th Earl of Lichfield (25 April 1939 – 11 November 2005), was an English photographer from the Anson family.
He inherited the Earldom of Lichfield in 1960 from his paternal grandfather.
In his professional practice he was known as Patrick Lichfield.
Biography

Thomas Patrick John Anson was born on 25 April 1939.
He was the only son of Lieutenant-Colonel Thomas William Arnold Anson, Viscount Anson (1913–1958), the eldest son and heir apparent of Thomas Edward Anson, 4th Earl of Lichfield (1883–1960).
His mother was born Anne Bowes-Lyon (1917–1980), a niece of Queen Elizabeth the Queen Mother.
His parents divorced in 1948, and his mother subsequently became Princess Anne of Denmark after her remarriage to Prince Georg of Denmark in 1950.
He had one sister, Lady Elizabeth Georgiana Anson (1941–2020), who married Sir Geoffrey Adam Shakerley, 6th Baronet.
Lichfield was educated at two boarding independent schools: Wellesley House School in the coastal town of Broadstairs in Kent, and Harrow School in Harrow on the Hill in north-west London, followed by the Royal Military Academy Sandhurst.
His father died in 1958, leaving Patrick to succeed as 5th Earl of Lichfield when his grandfather died in 1960.
Lichfield joined the Grenadier Guards in 1959.
He was selected to take the official photographs of the wedding of the Prince and Princess of Wales in 1981, and subsequently became one of the UK's best-known photographers.
He was chosen by Queen Elizabeth II and the Duke of Edinburgh to take official pictures of her Golden Jubilee in 2002.
He also cameoed in the British sitcom Keeping Up Appearances, appearing in the episode "Sea Fever" as a passenger on the Queen Elizabeth 2.
Lichfield resided in an apartment at the former family seat of Shugborough Hall, near Cannock Chase in Staffordshire.
Marriage and children

On 8 March 1975 Lichfield married Lady Leonora Grosvenor, elder daughter of Robert Grosvenor, 5th Duke of Westminster and Hon.
The Countess of Lichfield has not remarried and has retained her title.
She and the Earl had one son and two daughters together:


Lichfield's most recent partner was the biographer Lady Annunziata Asquith, daughter of Julian Asquith, 2nd Earl of Oxford and Asquith.
Death

On 10 November 2005, Lichfield suffered a major stroke and died the following day at the John Radcliffe Hospital in Oxford.
Lichfield's apartment at Shugborough now houses an exhibition of his work, together with a recreation of his studio.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

: a owl:Ontology ;
    dcterms:source <http://www.co-ode.org/roberts/family-tree.owl> .

:alsoKnownAs a owl:AnnotationProperty .

:formerlyKnownAs a owl:AnnotationProperty .

:hasBirthYear a rdfs:Datatype,
        owl:AnnotationProperty .

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

:isAuntOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isSisterOf :isParentOf ) .

:isUncleOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isBrotherOf :isParentOf ) .

:knownAs a owl:AnnotationProperty .

dcterms:source a owl:AnnotationProperty .

ns2:isRuleEnabled a owl:AnnotationProperty .

:hasBrother a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isBrotherOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasDaughter a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isDaughterOf .

:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Man ;
    rdfs:subPropertyOf :hasParent ;
    owl:inverseOf :isFatherOf .

:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Woman ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf ;
    owl:inverseOf :isMotherOf .

:hasSister a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isSisterOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasSon a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isSonOf .

:isBloodrelationOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty .

:isDaughterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:isFatherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isMotherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isSonOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:DomainEntity a owl:Class .

:Female a owl:Class ;
    rdfs:subClassOf :Sex ;
    owl:disjointWith :Male .

:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf :isAncestorOf .

:isBrotherOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:Male a owl:Class ;
    rdfs:subClassOf :Sex .

:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person .

:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Sex .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns1:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns1:Variable .

:Ancestor a owl:Class ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :isAncestorOf ;
                        owl:someValuesFrom :Person ] ) ] .

:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty :hasFather ;
            owl:someValuesFrom :Man ],
        [ a owl:Restriction ;
            owl:onProperty :hasMother ;
            owl:someValuesFrom :Woman ],
        [ a owl:Restriction ;
            owl:onProperty :hasSex ;
            owl:someValuesFrom :Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass :Person ;
            owl:onProperty :hasParent ],
        :DomainEntity ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Man :Woman ) ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (d1847df6-df28-4af0-bd78-39a4eb89126c)
 Call ID: d1847df6-df28-4af0-bd78-39a4eb89126c
  Args:
    source: Thomas_Patrick_John_Anson
    type: :Man
  AssignClass (13edc7ca-d8ab-4cd2-9467-97a5d5b8951d)
 Call ID: 13edc7ca-d8ab-4cd2-9467-97a5d5b8951d
  Args:
    source: Thomas_Patrick_John_Anson
    type: :Person
  AddLiteral (f29dc816-fbfa-4449-8d1d-b3cdc39f88f9)
 Call ID: f29dc816-fbfa-4449-8d1d-b3cdc39f88f9
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1939
    source: Thomas_Patrick_John_Anson
  AddLiteral (4189d2e3-b514-4fa4-88f8-f3d76148d2c4)
 Call ID: 4189d2e3-b514-4fa4-88f8-f3d76148d2c4
  Args:
    literal_value: 2005
    source: Thomas_Patrick_John_Anson
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddLiteral (dd8f8af8-6ddc-4754-8fec-3315afe6246d)
 Call ID: dd8f8af8-6ddc-4754-8fec-3315afe6246d
  Args:
    literal_type: xsd:string
    relation: :knownAs
    literal_value: Patrick Lichfield
    source: Thomas_Patrick_John_Anson
  AssignClass (44b8d0e1-cda5-4844-aae2-35c1214de04f)
 Call ID: 44b8d0e1-cda5-4844-aae2-35c1214de04f
  Args:
    type: :Man
    source: Thomas_William_Arnold_Anson
  AssignClass (02ecb5c6-ee3d-4b5c-bfd4-26029375b986)
 Call ID: 02ecb5c6-ee3d-4b5c-bfd4-26029375b986
  Args:
    type: :Person
    source: Thomas_William_Arnold_Anson
  AddLiteral (08eb4328-fb1a-4c98-b5a4-b54b7a33e188)
 Call ID: 08eb4328-fb1a-4c98-b5a4-b54b7a33e188
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1913
    source: Thomas_William_Arnold_Anson
  AddLiteral (c897e447-3f34-402c-b76b-f190f9d3ca24)
 Call ID: c897e447-3f34-402c-b76b-f190f9d3ca24
  Args:
    source: Thomas_William_Arnold_Anson
    literal_value: 1958
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddTriple (89c00a6a-c915-4ba4-a053-58144e1bf981)
 Call ID: 89c00a6a-c915-4ba4-a053-58144e1bf981
  Args:
    relation: :hasFather
    target: Thomas_William_Arnold_Anson
    source: Thomas_Patrick_John_Anson
  AssignClass (b8b80ac2-075c-49ff-8a24-d9350c979105)
 Call ID: b8b80ac2-075c-49ff-8a24-d9350c979105
  Args:
    type: :Man
    source: Thomas_Edward_Anson
  AssignClass (17bc6a07-8fa7-4884-b85e-8f60904c46ee)
 Call ID: 17bc6a07-8fa7-4884-b85e-8f60904c46ee
  Args:
    source: Thomas_Edward_Anson
    type: :Person
  AddLiteral (906f47eb-d0da-4603-b644-35ce2417b599)
 Call ID: 906f47eb-d0da-4603-b644-35ce2417b599
  Args:
    source: Thomas_Edward_Anson
    literal_value: 1883
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (24975153-48ab-47c1-ba46-1c9a35ccb56d)
 Call ID: 24975153-48ab-47c1-ba46-1c9a35ccb56d
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1960
    source: Thomas_Edward_Anson
  AddTriple (c9cbd5f1-9e5d-4939-8374-9c8027dd72ce)
 Call ID: c9cbd5f1-9e5d-4939-8374-9c8027dd72ce
  Args:
    relation: :hasFather
    source: Thomas_William_Arnold_Anson
    target: Thomas_Edward_Anson
  AssignClass (f27fd45b-c99c-4460-b264-5e970e0a9982)
 Call ID: f27fd45b-c99c-4460-b264-5e970e0a9982
  Args:
    type: :Woman
    source: Anne_Bowes-Lyon
  AssignClass (d470ddbb-e789-47be-8c62-29f9e3575944)
 Call ID: d470ddbb-e789-47be-8c62-29f9e3575944
  Args:
    type: :Person
    source: Anne_Bowes-Lyon
  AddLiteral (6dd15a5c-5733-45d9-98ab-97701290550c)
 Call ID: 6dd15a5c-5733-45d9-98ab-97701290550c
  Args:
    literal_value: 1917
    source: Anne_Bowes-Lyon
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (958e2bc6-fe33-4d8a-9a49-cbeee65540d7)
 Call ID: 958e2bc6-fe33-4d8a-9a49-cbeee65540d7
  Args:
    literal_value: 1980
    source: Anne_Bowes-Lyon
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddTriple (b52b4342-f13c-41db-88f5-665346f513a1)
 Call ID: b52b4342-f13c-41db-88f5-665346f513a1
  Args:
    relation: :hasMother
    source: Thomas_Patrick_John_Anson
    target: Anne_Bowes-Lyon
  AssignClass (3bb0e1c2-a0a3-489d-a67a-5b4546aa787a)
 Call ID: 3bb0e1c2-a0a3-489d-a67a-5b4546aa787a
  Args:
    source: Lady_Elizabeth_Georgiana_Anson
    type: :Woman
  AssignClass (c8d9a0a6-a11e-4d78-9a43-79570522938e)
 Call ID: c8d9a0a6-a11e-4d78-9a43-79570522938e
  Args:
    type: :Person
    source: Lady_Elizabeth_Georgiana_Anson
  AddLiteral (a7f8bc81-8a68-4007-908a-295a44db12b2)
 Call ID: a7f8bc81-8a68-4007-908a-295a44db12b2
  Args:
    source: Lady_Elizabeth_Georgiana_Anson
    literal_value: 1941
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (c25707ab-2cd9-4ab1-aec6-1361d35b5da8)
 Call ID: c25707ab-2cd9-4ab1-aec6-1361d35b5da8
  Args:
    source: Lady_Elizabeth_Georgiana_Anson
    literal_value: 2020
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddTriple (f69301d1-7806-4ea5-a58b-a907ccd94054)
 Call ID: f69301d1-7806-4ea5-a58b-a907ccd94054
  Args:
    relation: :hasSister
    target: Lady_Elizabeth_Georgiana_Anson
    source: Thomas_Patrick_John_Anson
  AddTriple (ea78da8a-1c25-4db5-ae2b-c9a9b6d4fae5)
 Call ID: ea78da8a-1c25-4db5-ae2b-c9a9b6d4fae5
  Args:
    relation: :hasMother
    target: Anne_Bowes-Lyon
    source: Lady_Elizabeth_Georgiana_Anson
  AddTriple (df31738e-5c4d-4606-a8af-8558f04fa5d3)
 Call ID: df31738e-5c4d-4606-a8af-8558f04fa5d3
  Args:
    source: Lady_Elizabeth_Georgiana_Anson
    target: Thomas_William_Arnold_Anson
    relation: :hasFather
  AssignClass (28cde177-4dc9-461b-b714-731c8ddc8b56)
 Call ID: 28cde177-4dc9-461b-b714-731c8ddc8b56
  Args:
    type: :Woman
    source: Lady_Leonora_Grosvenor
  AssignClass (f24a6eb5-f802-42c4-b557-409bfa286023)
 Call ID: f24a6eb5-f802-42c4-b557-409bfa286023
  Args:
    type: :Person
    source: Lady_Leonora_Grosvenor
  AddLiteral (435dca11-d6cf-4b2a-8978-f82506dec0a4)
 Call ID: 435dca11-d6cf-4b2a-8978-f82506dec0a4
  Args:
    literal_value: 1975
    source: Thomas_Patrick_John_Anson
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (e3491ad4-88e4-4ba8-9c9a-3c3288f908fd)
 Call ID: e3491ad4-88e4-4ba8-9c9a-3c3288f908fd
  Args:
    relation: :hasRelation
    target: Lady_Leonora_Grosvenor
    source: Thomas_Patrick_John_Anson
  AssignClass (a88bd995-c16f-4698-9b65-d7def4c27e8f)
 Call ID: a88bd995-c16f-4698-9b65-d7def4c27e8f
  Args:
    source: Robert_Grosvenor
    type: :Man
  AssignClass (9e76d049-accc-4f8d-b909-acefef207305)
 Call ID: 9e76d049-accc-4f8d-b909-acefef207305
  Args:
    type: :Person
    source: Robert_Grosvenor
  AddTriple (7bd66556-82cb-4193-9780-34b9c2a0a1cd)
 Call ID: 7bd66556-82cb-4193-9780-34b9c2a0a1cd
  Args:
    relation: :hasFather
    source: Lady_Leonora_Grosvenor
    target: Robert_Grosvenor
  AssignClass (708e0848-6610-42e6-b01c-b617bb482c35)
 Call ID: 708e0848-6610-42e6-b01c-b617bb482c35
  Args:
    source: Lady_Annunziata_Asquith
    type: :Woman
  AssignClass (9d762212-df10-4703-af60-ae1653ed48de)
 Call ID: 9d762212-df10-4703-af60-ae1653ed48de
  Args:
    type: :Person
    source: Lady_Annunziata_Asquith
  AddTriple (ef76d96e-8a12-4023-88c1-4927d05c1902)
 Call ID: ef76d96e-8a12-4023-88c1-4927d05c1902
  Args:
    relation: :hasRelation
    source: Thomas_Patrick_John_Anson
    target: Lady_Annunziata_Asquith
  AssignClass (afad72de-5cb8-4692-8155-6da21532a299)
 Call ID: afad72de-5cb8-4692-8155-6da21532a299
  Args:
    type: :Man
    source: Julian_Asquith
  AssignClass (a9da8357-a13f-404c-ab4e-81b4b7fdbeeb)
 Call ID: a9da8357-a13f-404c-ab4e-81b4b7fdbeeb
  Args:
    type: :Person
    source: Julian_Asquith
  AddTriple (695dc7c5-51e1-4773-8631-dbea88b8dfbe)
 Call ID: 695dc7c5-51e1-4773-8631-dbea88b8dfbe
  Args:
    relation: :hasFather
    target: Julian_Asquith
    source: Lady_Annunziata_Asquith
  Finish (280f3bfb-8057-472b-b093-d331dd53a92f)
 Call ID: 280f3bfb-8057-472b-b093-d331dd53a92f
  Args: