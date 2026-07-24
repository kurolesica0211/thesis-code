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
Alfonso, Prince of Asturias (10 May 1907 – 6 September 1938), was heir apparent to the throne of Spain from birth until the abolition of the monarchy in 1931.
Alfonso was the eldest son of King Alfonso XIII of Spain and Victoria Eugenie of Battenberg.
Alfonso's renunciation of his rights as heir to the Spanish throne in order to marry Cuban commoner Edelmira Sampedro caused controversy at the time.
Though appearing to have sustained minor injuries, his haemophilia, inherited through his great-grandmother Queen Victoria, led to fatal internal bleeding.
Early life

Alfonso was the eldest child of the then-reigning King Alfonso XIII and Victoria Eugenie of Battenberg.
As decreed by custom, he was registered by the Marquis of Figueroa, Minister of Justice, in the Civil Registry of the Royal Family as Alfonso Pío Cristino Eduardo Francisco Guillermo Carlos Enrique Eugenio Fernando Antonio Venancio.
Eight days after his birth, Alfonso was christened in the royal chapel of the Royal Palace of Madrid by the Archbishop of Toledo.
Prince Arthur, Duke of Connaught, Prince Friedrich Leopold of Prussia, Archduke Eugen of Austria and Afonso, Duke of Porto, were also present.
Alfonso's father faced increasing political problems that led Spain to become a republic in 1931 when the monarch was deposed.
Renunciation and marriages

There had been plans for young Alfonso's deposition from succession, but ultimately he himself renounced his rights to the then-defunct throne to marry a commoner, Edelmira Sampedro y Robato, religiously in Ouchy on 21 June 1933, after which Alfonso took the courtesy title Count of Covadonga.
In a civil ceremony on 3 July 1937, Alfonso married another commoner, Marta Esther Rocafort-Altuzarra, in Havana.
However, Alfonso de Bourbon, a resident of California, later claimed to be an illegitimate son of Alfonso.
In 1938, Alfonso, then resident in the United States, publicly stated his readiness to accept the Spanish crown if called on to do so.
This action reversed Alfonso's renunciation of 1933 and led to his being disavowed by his father King Alfonso.
Death

A car crash led to Alfonso's early death on September 6, 1938, at the age of 31.
The car crashed into a telephone booth and Alfonso appeared to have only minor injuries, but his haemophilia led to fatal internal bleeding.
Alfonso’s youngest brother, Gonzalo, had died just over four years before under very similar circumstances—having also inherited hemophilia, he was involved in a crash after the automobile he was in swerved to avoid a cyclist.
Alfonso was entombed at Woodlawn Park Cemetery and Mausoleum (now Caballero Rivero Woodlawn Park North Cemetery and Mausoleum) in Miami, and was re-entombed in 1985 at the Pantheon of the Princes in El Escorial.
Alfonso was the 1,120th Knight of the Order of the Golden Fleece in Spain and Knight with Collar of the Order of Charles III, inducted as both shortly after his birth in 1907.



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
  AssignClass (ec1cbd1b-81d1-450f-ab4f-978dc13b352f)
 Call ID: ec1cbd1b-81d1-450f-ab4f-978dc13b352f
  Args:
    type: :Person
    source: Alfonso_Prince_of_Asturias
  AssignClass (6fd7cd88-f45f-47e5-9fef-360ec40cace7)
 Call ID: 6fd7cd88-f45f-47e5-9fef-360ec40cace7
  Args:
    source: Alfonso_Prince_of_Asturias
    type: :Man
  AssignClass (a8c1278f-c3df-4756-8e2e-c75e406c8f51)
 Call ID: a8c1278f-c3df-4756-8e2e-c75e406c8f51
  Args:
    source: Alfonso_XIII_of_Spain
    type: :Person
  AssignClass (a76f7abd-8979-4e4f-bc24-36bb3006ca8b)
 Call ID: a76f7abd-8979-4e4f-bc24-36bb3006ca8b
  Args:
    source: Alfonso_XIII_of_Spain
    type: :Man
  AssignClass (f4cecc1d-7089-47cc-b814-b1b967142eec)
 Call ID: f4cecc1d-7089-47cc-b814-b1b967142eec
  Args:
    type: :Person
    source: Victoria_Eugenie_of_Battenberg
  AssignClass (c166d3da-8cb0-44a3-bdb1-dbb3be22316a)
 Call ID: c166d3da-8cb0-44a3-bdb1-dbb3be22316a
  Args:
    source: Victoria_Eugenie_of_Battenberg
    type: :Woman
  AssignClass (f8589899-c1fc-4985-affd-e65ae692699a)
 Call ID: f8589899-c1fc-4985-affd-e65ae692699a
  Args:
    type: :Person
    source: Edelmira_Sampedro
  AssignClass (6a87bf48-5acc-4560-9c33-822417f00b1a)
 Call ID: 6a87bf48-5acc-4560-9c33-822417f00b1a
  Args:
    source: Edelmira_Sampedro
    type: :Woman
  AssignClass (ca4a1b3e-2523-4d01-ad44-0f0e63e6bb80)
 Call ID: ca4a1b3e-2523-4d01-ad44-0f0e63e6bb80
  Args:
    type: :Person
    source: Marta_Esther_Rocafort-Altuzarra
  AssignClass (65d5e381-a677-49d5-b009-472b658938cc)
 Call ID: 65d5e381-a677-49d5-b009-472b658938cc
  Args:
    source: Marta_Esther_Rocafort-Altuzarra
    type: :Woman
  AssignClass (b0738509-b322-4faf-bd30-aaf842af9839)
 Call ID: b0738509-b322-4faf-bd30-aaf842af9839
  Args:
    type: :Person
    source: Alfonso_de_Bourbon
  AssignClass (2d90290a-b894-40f1-bb98-efb1d206ef52)
 Call ID: 2d90290a-b894-40f1-bb98-efb1d206ef52
  Args:
    type: :Man
    source: Alfonso_de_Bourbon
  AssignClass (07c3c4a4-99a8-48c3-a185-51f591e2cfa3)
 Call ID: 07c3c4a4-99a8-48c3-a185-51f591e2cfa3
  Args:
    type: :Person
    source: Gonzalo
  AssignClass (018a2bfe-4820-44c8-8c00-d0968658964f)
 Call ID: 018a2bfe-4820-44c8-8c00-d0968658964f
  Args:
    type: :Man
    source: Gonzalo
  AddLiteral (82967ddc-d60d-4b8d-95f4-65259f196f7d)
 Call ID: 82967ddc-d60d-4b8d-95f4-65259f196f7d
  Args:
    source: Alfonso_Prince_of_Asturias
    literal_value: 1907
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (9fddb9fd-3794-49f4-9b10-6d5584bcaafa)
 Call ID: 9fddb9fd-3794-49f4-9b10-6d5584bcaafa
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1938
    source: Alfonso_Prince_of_Asturias
  AddTriple (79427bac-85e9-4aed-9e7f-fd5fb7a891e5)
 Call ID: 79427bac-85e9-4aed-9e7f-fd5fb7a891e5
  Args:
    relation: :hasFather
    target: Alfonso_XIII_of_Spain
    source: Alfonso_Prince_of_Asturias
  AddTriple (58bdfa50-1dd9-4228-b41b-b28b0c8e1d5c)
 Call ID: 58bdfa50-1dd9-4228-b41b-b28b0c8e1d5c
  Args:
    relation: :hasMother
    target: Victoria_Eugenie_of_Battenberg
    source: Alfonso_Prince_of_Asturias
  AddTriple (07283369-360c-40fd-a943-862e3431d151)
 Call ID: 07283369-360c-40fd-a943-862e3431d151
  Args:
    target: Gonzalo
    source: Alfonso_Prince_of_Asturias
    relation: :hasBrother
  AddLiteral (011dc389-49be-42f6-9ef5-6eaa81b0b43b)
 Call ID: 011dc389-49be-42f6-9ef5-6eaa81b0b43b
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1933
    source: Alfonso_Prince_of_Asturias
  AddTriple (56b04750-5915-4324-a6e0-7a82d0f3e845)
 Call ID: 56b04750-5915-4324-a6e0-7a82d0f3e845
  Args:
    relation: :hasRelation
    source: Alfonso_Prince_of_Asturias
    target: Edelmira_Sampedro
  AddLiteral (bc9c4fb5-3e67-4a3f-889f-d57e5900e361)
 Call ID: bc9c4fb5-3e67-4a3f-889f-d57e5900e361
  Args:
    literal_value: 1937
    source: Alfonso_Prince_of_Asturias
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (96ede31f-7a1d-489e-b0a2-ec6601809b4c)
 Call ID: 96ede31f-7a1d-489e-b0a2-ec6601809b4c
  Args:
    relation: :hasRelation
    target: Marta_Esther_Rocafort-Altuzarra
    source: Alfonso_Prince_of_Asturias
  Finish (a85ad180-d4eb-44c8-81c1-5e92779cf77e)
 Call ID: a85ad180-d4eb-44c8-81c1-5e92779cf77e
  Args: