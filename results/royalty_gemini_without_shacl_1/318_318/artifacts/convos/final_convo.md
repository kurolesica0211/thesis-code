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
  AssignClass (a746dce7-3908-433a-be7c-5c0c4df30b05)
 Call ID: a746dce7-3908-433a-be7c-5c0c4df30b05
  Args:
    source: Alfonso_Prince_of_Asturias
    type: :Man
  AssignClass (9dd8d0e4-d429-476b-a610-f0bf4f5d07ee)
 Call ID: 9dd8d0e4-d429-476b-a610-f0bf4f5d07ee
  Args:
    source: Alfonso_Prince_of_Asturias
    type: :Person
  AssignClass (58689e19-9ff6-4d9f-9208-bb8907503ce6)
 Call ID: 58689e19-9ff6-4d9f-9208-bb8907503ce6
  Args:
    source: Alfonso_XIII_of_Spain
    type: :Man
  AssignClass (abbe9bb3-8316-439e-bd80-f4090b1b0dde)
 Call ID: abbe9bb3-8316-439e-bd80-f4090b1b0dde
  Args:
    type: :Person
    source: Alfonso_XIII_of_Spain
  AssignClass (c88d5d5a-235d-4b17-8598-b115b16f1446)
 Call ID: c88d5d5a-235d-4b17-8598-b115b16f1446
  Args:
    source: Victoria_Eugenie_of_Battenberg
    type: :Woman
  AssignClass (516eae73-1d54-4a74-a33e-51903b4760ab)
 Call ID: 516eae73-1d54-4a74-a33e-51903b4760ab
  Args:
    type: :Person
    source: Victoria_Eugenie_of_Battenberg
  AssignClass (988c1647-de0b-43d9-8f33-0e7370dd17de)
 Call ID: 988c1647-de0b-43d9-8f33-0e7370dd17de
  Args:
    type: :Woman
    source: Edelmira_Sampedro_y_Robato
  AssignClass (499725ea-b15e-4a2e-92d4-8c2afe17ebb8)
 Call ID: 499725ea-b15e-4a2e-92d4-8c2afe17ebb8
  Args:
    source: Edelmira_Sampedro_y_Robato
    type: :Person
  AssignClass (b32f9f74-6d76-4d6b-8198-20b4d7561682)
 Call ID: b32f9f74-6d76-4d6b-8198-20b4d7561682
  Args:
    type: :Woman
    source: Marta_Esther_Rocafort-Altuzarra
  AssignClass (17e611a8-48c9-45fb-a83f-a66bb3252380)
 Call ID: 17e611a8-48c9-45fb-a83f-a66bb3252380
  Args:
    type: :Person
    source: Marta_Esther_Rocafort-Altuzarra
  AssignClass (c0c6e364-deec-490e-8cf1-9b5d78bc4e9b)
 Call ID: c0c6e364-deec-490e-8cf1-9b5d78bc4e9b
  Args:
    source: Alfonso_de_Bourbon
    type: :Man
  AssignClass (ed34fb95-ebc4-4b9f-a666-a77360a3c48d)
 Call ID: ed34fb95-ebc4-4b9f-a666-a77360a3c48d
  Args:
    source: Alfonso_de_Bourbon
    type: :Person
  AssignClass (66daf30a-1dc1-46d1-a2f1-5720101e5416)
 Call ID: 66daf30a-1dc1-46d1-a2f1-5720101e5416
  Args:
    source: Gonzalo
    type: :Man
  AssignClass (933a559a-f98b-4229-a65e-f8497c7bc3ae)
 Call ID: 933a559a-f98b-4229-a65e-f8497c7bc3ae
  Args:
    source: Gonzalo
    type: :Person
  AddLiteral (65d778b2-30af-453f-9de0-b2d1dbc6f732)
 Call ID: 65d778b2-30af-453f-9de0-b2d1dbc6f732
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Alfonso_Prince_of_Asturias
    literal_value: 1907
  AddLiteral (9979f103-3457-4acc-a32a-c48b0b7817de)
 Call ID: 9979f103-3457-4acc-a32a-c48b0b7817de
  Args:
    literal_value: 1938
    source: Alfonso_Prince_of_Asturias
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddTriple (c68f8037-93e2-4a45-9d22-12b2bf7e2b46)
 Call ID: c68f8037-93e2-4a45-9d22-12b2bf7e2b46
  Args:
    target: Alfonso_XIII_of_Spain
    relation: :hasFather
    source: Alfonso_Prince_of_Asturias
  AddTriple (f5c5b800-adbd-4ea3-91fb-d5504b2b0719)
 Call ID: f5c5b800-adbd-4ea3-91fb-d5504b2b0719
  Args:
    target: Victoria_Eugenie_of_Battenberg
    relation: :hasMother
    source: Alfonso_Prince_of_Asturias
  AddTriple (6c00c5cd-1d27-45f7-b91d-4bfa2d9127f4)
 Call ID: 6c00c5cd-1d27-45f7-b91d-4bfa2d9127f4
  Args:
    source: Alfonso_Prince_of_Asturias
    relation: :isSiblingOf
    target: Gonzalo
  AddLiteral (3f036173-43f2-4baf-b632-44ebe28ff4b0)
 Call ID: 3f036173-43f2-4baf-b632-44ebe28ff4b0
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Alfonso_Prince_of_Asturias
    literal_value: 1933
  AddTriple (aaf8e595-6966-46d8-b7d1-3fd7c1f40876)
 Call ID: aaf8e595-6966-46d8-b7d1-3fd7c1f40876
  Args:
    target: Edelmira_Sampedro_y_Robato
    source: Alfonso_Prince_of_Asturias
    relation: :hasRelation
  AddLiteral (e24311e2-be92-4249-b031-44d5781739db)
 Call ID: e24311e2-be92-4249-b031-44d5781739db
  Args:
    literal_value: 1937
    relation: :hasMarriageYear
    source: Alfonso_Prince_of_Asturias
    literal_type: xsd:integer
  AddTriple (266ea71d-5845-4f5e-acc0-5110d82bc1fe)
 Call ID: 266ea71d-5845-4f5e-acc0-5110d82bc1fe
  Args:
    relation: :hasRelation
    source: Alfonso_Prince_of_Asturias
    target: Marta_Esther_Rocafort-Altuzarra
  AddTriple (9b561254-a40c-4a02-b51f-c565ffd9ca6a)
 Call ID: 9b561254-a40c-4a02-b51f-c565ffd9ca6a
  Args:
    target: Alfonso_Prince_of_Asturias
    relation: :isSonOf
    source: Alfonso_de_Bourbon
  Finish (2c01a500-7acb-4332-8f49-67b22ab97ee6)
 Call ID: 2c01a500-7acb-4332-8f49-67b22ab97ee6
  Args: