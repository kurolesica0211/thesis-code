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
Grand Duke HenriGrand Duchess Maria Teresa


Princess Joan


Descendants of Prince Felix and also members of the Grand Ducal Family of Luxembourg:


Princess Joan


Descendants of Prince René:


Princess Maria Pia


Princess Marina


Descendants of Prince Louis:


Prince RémyPrincess Elisabeth


Princess Chantal
Prince JeanPrincess Virginia


Prince Guillaume of Luxembourg (Guillaume Marie Louis Christian; born 1 May 1963) is the third son and youngest child of Grand Duke Jean and Grand Duchess Josephine-Charlotte of Luxembourg.
On the night of 10 to 11 September 2000, Prince Guillaume and Princess Sibilla were involved in a serious car accident near Paris.
Marriage and children

Prince Guillaume married Sibilla Sandra Weiller y Torlonia (b. 12 June 1968, Neuilly-sur-Seine, France), the second child of French industrialist and patron of the Arts Paul-Annik Weiller (son of Paul-Louis Weiller and Aliki, Lady Russell) and Italian noblewoman Donna Olimpia Torlonia di Civitella-Cesi (daughter of Alessandro Torlonia, 5th Prince of Civitella-Cesi and Infanta Beatriz of Spain) and the second cousin of King Felipe VI of Spain civilly in Sélestat on 8 September 1994 and religiously at Versailles Cathedral on 24 September 1994, who received the title "Princess of Luxembourg".
Guillaume and Sibilla have four children:


Their sons are in the line of succession to the throne of Luxembourg.
Prince Guillaume is godfather to his nephew, Guillaume V, Grand Duke of Luxembourg.
He is also one of the godparents of Prince Achileas-Andreas of Greece and Denmark, the second son of Pavlos, Crown Prince of Greece.



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
  AssignClass (b606a5c1-8349-4cc4-950e-65c531950489)
 Call ID: b606a5c1-8349-4cc4-950e-65c531950489
  Args:
    type: :Man
    source: :GrandDukeHenri
  AssignClass (6b8ece13-c40e-4f92-9031-0db5df1c2b63)
 Call ID: 6b8ece13-c40e-4f92-9031-0db5df1c2b63
  Args:
    type: :Woman
    source: :GrandDuchessMariaTeresa
  AssignClass (abe824bc-4435-4138-acc5-8c4c96b81c4a)
 Call ID: abe824bc-4435-4138-acc5-8c4c96b81c4a
  Args:
    type: :Woman
    source: :PrincessJoan
  AssignClass (6c44cd4b-d6ed-4a7f-817e-ff61d0a65b07)
 Call ID: 6c44cd4b-d6ed-4a7f-817e-ff61d0a65b07
  Args:
    source: :PrinceFelix
    type: :Man
  AssignClass (58f8394e-aaa9-4364-925b-b2e614312441)
 Call ID: 58f8394e-aaa9-4364-925b-b2e614312441
  Args:
    type: :Man
    source: :PrinceRené
  AssignClass (31f54409-7d69-46ca-b3cc-8ce23dcf78f2)
 Call ID: 31f54409-7d69-46ca-b3cc-8ce23dcf78f2
  Args:
    source: :PrincessMariaPia
    type: :Woman
  AssignClass (1dbe30ba-9c69-4a71-aef5-2053a1cdafb6)
 Call ID: 1dbe30ba-9c69-4a71-aef5-2053a1cdafb6
  Args:
    source: :PrincessMarina
    type: :Woman
  AssignClass (9bf30602-f9e9-4c8c-b337-1f8740920dd6)
 Call ID: 9bf30602-f9e9-4c8c-b337-1f8740920dd6
  Args:
    source: :PrinceLouis
    type: :Man
  AssignClass (18e8c2d1-6e59-42e8-92bf-261511854733)
 Call ID: 18e8c2d1-6e59-42e8-92bf-261511854733
  Args:
    source: :PrinceRémy
    type: :Man
  AssignClass (35d02f5d-c9d5-494c-8649-450c3e00d65d)
 Call ID: 35d02f5d-c9d5-494c-8649-450c3e00d65d
  Args:
    type: :Woman
    source: :PrincessElisabeth
  AssignClass (0fb9e2a7-10a5-4d73-8081-f3580b57c71a)
 Call ID: 0fb9e2a7-10a5-4d73-8081-f3580b57c71a
  Args:
    source: :PrincessChantal
    type: :Woman
  AssignClass (9739a76d-ec42-4f91-babc-3f7f19b54fc3)
 Call ID: 9739a76d-ec42-4f91-babc-3f7f19b54fc3
  Args:
    source: :PrinceJean
    type: :Man
  AssignClass (ae5c988c-95f2-45ef-8141-2fa4a731e307)
 Call ID: ae5c988c-95f2-45ef-8141-2fa4a731e307
  Args:
    type: :Woman
    source: :PrincessVirginia
  AssignClass (64fd28b3-a944-48e4-a632-faab85c2d749)
 Call ID: 64fd28b3-a944-48e4-a632-faab85c2d749
  Args:
    source: :PrinceGuillaumeLuxembourg
    type: :Man
  AssignClass (fec0f230-5b0a-4463-a5af-b40cdb00373a)
 Call ID: fec0f230-5b0a-4463-a5af-b40cdb00373a
  Args:
    type: :Man
    source: :GrandDukeJean
  AssignClass (1beb4d26-01eb-48c7-8ece-64ccba72b6ae)
 Call ID: 1beb4d26-01eb-48c7-8ece-64ccba72b6ae
  Args:
    source: :GrandDuchessJosephineCharlotte
    type: :Woman
  AssignClass (290f7500-5999-4b22-a80e-f2fee23157a4)
 Call ID: 290f7500-5999-4b22-a80e-f2fee23157a4
  Args:
    type: :Woman
    source: :PrincessSibilla
  AssignClass (6bddb033-c634-487b-9a1d-54f71841d3bb)
 Call ID: 6bddb033-c634-487b-9a1d-54f71841d3bb
  Args:
    type: :Man
    source: :PaulAnnikWeiller
  AssignClass (628119e9-a406-430f-8cf3-8b31a9084fbb)
 Call ID: 628119e9-a406-430f-8cf3-8b31a9084fbb
  Args:
    source: :PaulLouisWeiller
    type: :Man
  AssignClass (352087ac-85f4-4bdf-b530-bb5d9594a0f7)
 Call ID: 352087ac-85f4-4bdf-b530-bb5d9594a0f7
  Args:
    source: :AlikiLadyRussell
    type: :Woman
  AssignClass (22f1ebbc-64b6-4846-8919-0680eadce12a)
 Call ID: 22f1ebbc-64b6-4846-8919-0680eadce12a
  Args:
    source: :DonnaOlimpiaTorlonia
    type: :Woman
  AssignClass (bccc3f5e-2f84-4cf0-819d-1180e5863fdd)
 Call ID: bccc3f5e-2f84-4cf0-819d-1180e5863fdd
  Args:
    source: :AlessandroTorlonia
    type: :Man
  AssignClass (2cf99e97-4822-4a86-bf1a-b40a48eed937)
 Call ID: 2cf99e97-4822-4a86-bf1a-b40a48eed937
  Args:
    type: :Woman
    source: :InfantaBeatriz
  AddLiteral (124fe8e1-3c6b-46f4-884c-8709abce3a33)
 Call ID: 124fe8e1-3c6b-46f4-884c-8709abce3a33
  Args:
    literal_value: 1963
    source: :PrinceGuillaumeLuxembourg
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddTriple (c0910499-f305-425d-a73d-1ddfe5c21c8e)
 Call ID: c0910499-f305-425d-a73d-1ddfe5c21c8e
  Args:
    source: :PrinceGuillaumeLuxembourg
    target: :GrandDukeJean
    relation: :hasFather
  AddTriple (1f0f9e1f-f940-4787-b365-1754b1917f43)
 Call ID: 1f0f9e1f-f940-4787-b365-1754b1917f43
  Args:
    source: :PrinceGuillaumeLuxembourg
    target: :GrandDuchessJosephineCharlotte
    relation: :hasMother
  AddTriple (23f5a579-0192-45e9-9671-dcf9cb4a7270)
 Call ID: 23f5a579-0192-45e9-9671-dcf9cb4a7270
  Args:
    relation: :hasFather
    target: :PaulAnnikWeiller
    source: :PrincessSibilla
  AddTriple (fb1b86c1-809c-4db3-946a-09b171ecd844)
 Call ID: fb1b86c1-809c-4db3-946a-09b171ecd844
  Args:
    target: :DonnaOlimpiaTorlonia
    source: :PrincessSibilla
    relation: :hasMother
  AddTriple (0a9a79b4-9a71-4dc8-8cb0-3c5f5d5be3d3)
 Call ID: 0a9a79b4-9a71-4dc8-8cb0-3c5f5d5be3d3
  Args:
    relation: :hasFather
    target: :PaulLouisWeiller
    source: :PaulAnnikWeiller
  AddTriple (239d6e08-0233-4c9a-a413-0c7ee2f40478)
 Call ID: 239d6e08-0233-4c9a-a413-0c7ee2f40478
  Args:
    relation: :hasMother
    source: :PaulAnnikWeiller
    target: :AlikiLadyRussell
  AddTriple (c86ec965-3daa-4ce2-8ac1-58dc547315b0)
 Call ID: c86ec965-3daa-4ce2-8ac1-58dc547315b0
  Args:
    target: :AlessandroTorlonia
    source: :DonnaOlimpiaTorlonia
    relation: :hasFather
  AddTriple (53449488-b613-4736-8c09-0c7a7af9a8ac)
 Call ID: 53449488-b613-4736-8c09-0c7a7af9a8ac
  Args:
    relation: :hasMother
    source: :DonnaOlimpiaTorlonia
    target: :InfantaBeatriz
  AddLiteral (48a6ebb6-b7a9-44ed-8e36-3f9f7bec54d7)
 Call ID: 48a6ebb6-b7a9-44ed-8e36-3f9f7bec54d7
  Args:
    relation: :hasMarriageYear
    source: :PrinceGuillaumeLuxembourg
    literal_type: xsd:integer
    literal_value: 1994
  AddTriple (a7173a78-cb08-4beb-8707-098131f01fdf)
 Call ID: a7173a78-cb08-4beb-8707-098131f01fdf
  Args:
    relation: :hasRelation
    target: :PrincessSibilla
    source: :PrinceGuillaumeLuxembourg
  Finish (310a3a71-b847-4e33-bb15-23e41c5f7ef0)
 Call ID: 310a3a71-b847-4e33-bb15-23e41c5f7ef0
  Args: