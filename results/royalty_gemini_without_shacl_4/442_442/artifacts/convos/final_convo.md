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
Princess Beatrix*


Princess Margriet*Pieter van Vollenhoven*


Prince Hugo de Bourbon de Parme (Carlos Hugo Roderik Sybren; born 20 January 1997), formerly Hugo Klynstra, is a member of the extended Dutch royal family as the son of Prince Carlos, Hereditary Duke of Parma.
He was the first great-grandchild of Queen Juliana of the Netherlands.
Born out of wedlock, he was denied titles and family rights by his father until the Dutch Council of State ruled in his favor in 2018, granting him the style and title of His Royal Highness Prince Carlos Hugo
Roderik Sybren de Bourbon de Parme.
Despite the ruling, he is neither a member of the Dutch royal house (although considered a member of the extended Dutch royal family) nor a member of the House of Bourbon-Parma and is not in the line of succession to the defunct Parmese throne.
Early life and family

Carlos Hugo Roderik Sybren Klynstra was born in Nijmegen on 20 January 1997 to Prince Carlos de Bourbon de Parme, Prince of Piacenza and his friend Brigitte Klynstra.
Due to being an illegitimate son, he was not born a prince.
His father told Dutch media that Hugo's birth was "his mother's wish" and an "independent decision", denying his son any family rights.
His maternal grandmother, Ingrid Pieksma-Klynstra, was the wife of Adolph Roderik Ernst Leopold, Count of Rechteren-Limpurg.
Through his father, he is a grandson of Carlos Hugo, Duke of Parma and Princess Irene of the Netherlands.
He is the first great-grandchild of Queen Juliana of the Netherlands and Prince Bernhard of Lippe-Biesterfeld.
He is also a great-grandson of Prince Xavier of Bourbon-Parma and Madeleine de Bourbon-Busset.
Upon the death of his grandfather, Carlos Hugo, in 2010, his father became the titular Duke of Parma and Piacenza, Carlist claimant to the Spanish throne, and the Head of the House of Bourbon-Parma.
According to a royal decree of Queen Beatrix in 1996, his father is also a Dutch prince.
He is the half-brother of Princess Luisa of Parma, Marchioness of Castell'Arquato, Princess Cecilia of Parma, Countess of Berceto and Prince Carlos of Parma, The Prince of Piacenza.
Legal dispute over title

Upon turning eighteen in 2015, Hugo went to court to have his surname changed from Klynstra to his father's surname, 'de Bourbon de Parme', and claimed the dutch noble title of prince.
The Hereditary Duke of Parma insisted that he had a formal agreement with Hugo's mother that their relationship was "no-strings-attached" and that there would be "no family entanglement" following Hugo's conception.
In 2016 the Ministry of Justice and Security ruled in favor of Hugo's claim and granted him the use of his father's surname.
On 28 February 2018, the Dutch Council of State ruled in Hugo's favor, stating that Dutch law on nobility was clear and that the circumstances of Hugo's birth are irrelevant, granting Hugo the right to claim both his father's surname and (dutch) noble title and address.
As such, he became His Royal Highness Prince Carlos Hugo Roderik Sybren de Bourbon de Parme.
The title of 'Prince(ss) de Bourbon de Parme' is a Dutch title, bestowed by Queen Beatrix in 1996, and does not mean that Hugo automatically became a member of the House of Bourbon-Parma.
The court ruling stated that membership to the House of Bourbon-Parma is "a private matter for the royal house itself".
As such, he is not in the line of succession to the defunct Parma throne.
Titles and styles

References




2 gave up the title "Prince of the Netherlands, but still held the title "Prince of Orange-Nassau"
3 title granted by Royal Decree to descendants of Princess Irene



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
  AssignClass (a1efc5da-6ba9-474f-a12e-3f5ea9f7dc89)
 Call ID: a1efc5da-6ba9-474f-a12e-3f5ea9f7dc89
  Args:
    source: Beatrix
    type: :Woman
  AssignClass (94a059e2-ae6b-4599-ad1b-cce07f8fdeeb)
 Call ID: 94a059e2-ae6b-4599-ad1b-cce07f8fdeeb
  Args:
    type: :Woman
    source: Margriet
  AssignClass (54393933-a93f-42b9-b53b-c8d2dacf265f)
 Call ID: 54393933-a93f-42b9-b53b-c8d2dacf265f
  Args:
    type: :Man
    source: Pieter van Vollenhoven
  AssignClass (440d20a2-6f24-4851-bf8e-adb7836b6374)
 Call ID: 440d20a2-6f24-4851-bf8e-adb7836b6374
  Args:
    source: Carlos Hugo Roderik Sybren de Bourbon de Parme
    type: :Man
  AssignClass (2ea4fd39-339d-4b82-9e9f-fc4dab9bd54a)
 Call ID: 2ea4fd39-339d-4b82-9e9f-fc4dab9bd54a
  Args:
    type: :Man
    source: Carlos de Bourbon de Parme
  AssignClass (0e6e1c22-d168-4d48-9ec2-03d63556a2d9)
 Call ID: 0e6e1c22-d168-4d48-9ec2-03d63556a2d9
  Args:
    type: :Woman
    source: Brigitte Klynstra
  AssignClass (379c321e-2bc0-4102-9c8e-3dc8ba14debe)
 Call ID: 379c321e-2bc0-4102-9c8e-3dc8ba14debe
  Args:
    source: Ingrid Pieksma-Klynstra
    type: :Woman
  AssignClass (48f643a4-1ae9-4901-859a-fafd8ec69cf6)
 Call ID: 48f643a4-1ae9-4901-859a-fafd8ec69cf6
  Args:
    type: :Man
    source: Adolph Roderik Ernst Leopold
  AssignClass (e1c63db0-a890-44c6-9492-f892a11af076)
 Call ID: e1c63db0-a890-44c6-9492-f892a11af076
  Args:
    source: Carlos Hugo, Duke of Parma
    type: :Man
  AssignClass (4b13fbf3-c192-4e16-87dc-04763121b024)
 Call ID: 4b13fbf3-c192-4e16-87dc-04763121b024
  Args:
    type: :Woman
    source: Irene of the Netherlands
  AssignClass (83cf617d-e78b-47e9-9498-3a94b9ed166d)
 Call ID: 83cf617d-e78b-47e9-9498-3a94b9ed166d
  Args:
    source: Juliana of the Netherlands
    type: :Woman
  AssignClass (cb732742-752a-4df9-acf0-509a1a98cb5b)
 Call ID: cb732742-752a-4df9-acf0-509a1a98cb5b
  Args:
    source: Bernhard of Lippe-Biesterfeld
    type: :Man
  AssignClass (acd1a135-a15d-4ac6-879a-7d1f6acb52b3)
 Call ID: acd1a135-a15d-4ac6-879a-7d1f6acb52b3
  Args:
    source: Xavier of Bourbon-Parma
    type: :Man
  AssignClass (bcc2437e-4aea-4cb2-b802-363184ed4734)
 Call ID: bcc2437e-4aea-4cb2-b802-363184ed4734
  Args:
    source: Madeleine de Bourbon-Busset
    type: :Woman
  AssignClass (3fee5278-9a18-40b3-922c-62a622ed6bed)
 Call ID: 3fee5278-9a18-40b3-922c-62a622ed6bed
  Args:
    source: Luisa of Parma
    type: :Woman
  AssignClass (6db60310-b1fb-4f20-b139-a45a1eaab98b)
 Call ID: 6db60310-b1fb-4f20-b139-a45a1eaab98b
  Args:
    type: :Woman
    source: Cecilia of Parma
  AssignClass (b89df85d-dd44-42c5-866c-dac0d3cb7cba)
 Call ID: b89df85d-dd44-42c5-866c-dac0d3cb7cba
  Args:
    type: :Man
    source: Carlos of Parma
  AddLiteral (e02aff77-d562-43e8-b283-6f66128aaaf7)
 Call ID: e02aff77-d562-43e8-b283-6f66128aaaf7
  Args:
    literal_value: Hugo Klynstra
    relation: :formerlyKnownAs
    source: Carlos Hugo Roderik Sybren de Bourbon de Parme
    literal_type: xsd:string
  AddLiteral (6dc14682-3e6f-440d-b834-c0666343af2f)
 Call ID: 6dc14682-3e6f-440d-b834-c0666343af2f
  Args:
    relation: :hasBirthYear
    literal_value: 1997
    source: Carlos Hugo Roderik Sybren de Bourbon de Parme
    literal_type: xsd:integer
  AddTriple (af6e63cc-c8de-4723-8157-f6059aa3766f)
 Call ID: af6e63cc-c8de-4723-8157-f6059aa3766f
  Args:
    target: Carlos de Bourbon de Parme
    source: Carlos Hugo Roderik Sybren de Bourbon de Parme
    relation: :hasFather
  AddTriple (b4a100ce-50e2-4f4b-9216-50dd5372e402)
 Call ID: b4a100ce-50e2-4f4b-9216-50dd5372e402
  Args:
    source: Carlos Hugo Roderik Sybren de Bourbon de Parme
    relation: :hasMother
    target: Brigitte Klynstra
  AddTriple (4894c32e-db9b-4df0-815a-590887f907b7)
 Call ID: 4894c32e-db9b-4df0-815a-590887f907b7
  Args:
    target: Ingrid Pieksma-Klynstra
    relation: :hasMother
    source: Brigitte Klynstra
  AddTriple (ba304086-56aa-4cda-9993-3e5d72891a4e)
 Call ID: ba304086-56aa-4cda-9993-3e5d72891a4e
  Args:
    target: Adolph Roderik Ernst Leopold
    source: Brigitte Klynstra
    relation: :hasFather
  AddTriple (bc4dd56b-e7ba-4ea2-af1b-8d1b113ce2e4)
 Call ID: bc4dd56b-e7ba-4ea2-af1b-8d1b113ce2e4
  Args:
    target: Carlos Hugo, Duke of Parma
    relation: :hasFather
    source: Carlos de Bourbon de Parme
  AddTriple (f97659f4-beb6-4ab6-947c-a5532977af62)
 Call ID: f97659f4-beb6-4ab6-947c-a5532977af62
  Args:
    source: Carlos de Bourbon de Parme
    relation: :hasMother
    target: Irene of the Netherlands
  AddTriple (f98cc75f-deb4-4e05-b82b-c83c47f56e71)
 Call ID: f98cc75f-deb4-4e05-b82b-c83c47f56e71
  Args:
    target: Xavier of Bourbon-Parma
    relation: :hasFather
    source: Carlos Hugo, Duke of Parma
  AddTriple (de03a533-7719-4bcd-8f36-9bbf511ba467)
 Call ID: de03a533-7719-4bcd-8f36-9bbf511ba467
  Args:
    target: Madeleine de Bourbon-Busset
    relation: :hasMother
    source: Carlos Hugo, Duke of Parma
  AddTriple (8f2363de-cfe0-46c0-bd0e-9852fd50c806)
 Call ID: 8f2363de-cfe0-46c0-bd0e-9852fd50c806
  Args:
    source: Irene of the Netherlands
    relation: :hasFather
    target: Bernhard of Lippe-Biesterfeld
  AddTriple (22bba006-020b-4310-a42e-a12de936fab7)
 Call ID: 22bba006-020b-4310-a42e-a12de936fab7
  Args:
    relation: :hasMother
    source: Irene of the Netherlands
    target: Juliana of the Netherlands
  AddTriple (f388e2f2-50e9-43e6-96e8-b4a952744014)
 Call ID: f388e2f2-50e9-43e6-96e8-b4a952744014
  Args:
    relation: :isSiblingOf
    source: Carlos Hugo Roderik Sybren de Bourbon de Parme
    target: Luisa of Parma
  AddTriple (ada354a3-b486-444b-8322-0818184df539)
 Call ID: ada354a3-b486-444b-8322-0818184df539
  Args:
    relation: :isSiblingOf
    source: Carlos Hugo Roderik Sybren de Bourbon de Parme
    target: Cecilia of Parma
  AddTriple (5d944a0b-8d5e-47d1-8db5-0d04682f8b75)
 Call ID: 5d944a0b-8d5e-47d1-8db5-0d04682f8b75
  Args:
    relation: :isSiblingOf
    source: Carlos Hugo Roderik Sybren de Bourbon de Parme
    target: Carlos of Parma
  Finish (7bc70933-683a-48ab-987d-dce3aac5157b)
 Call ID: 7bc70933-683a-48ab-987d-dce3aac5157b
  Args: