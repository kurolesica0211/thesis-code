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


Prince Bernhard Lucas Emmanuel of Orange-Nassau, van Vollenhoven (born 25 December 1969) is a Dutch racing driver, entrepreneur and member of the Dutch royal family.
He is the second son of Princess Margriet of the Netherlands and Pieter van Vollenhoven.
With Willem-Alexander's succession however, he is no longer a member of the Dutch Royal House, and is no longer in line to direct succession to the Dutch throne, but still retains his membership of the Dutch royal family 


Early life and education

Bernhard was born on 25 December 1969 in Nijmegen in the Netherlands.
He is the second son of Princess Margriet and Pieter van Vollenhoven.
He has three brothers: Princes Maurits, Pieter-Christiaan, and Floris.
Subsequently, in 1989 he attended Groningen University in the Netherlands where he studied marketing and market research.
Business

Bernhard is a self-employed entrepreneur.
In 2002, the name Ritzen Koeriers was changed to Logistieke Meesters, at which time Bernhard was no longer involved in the business.
Marriage and family

While studying in Groningen, Bernhard met Annette Sekrève, (born 18 April 1972).
They have three children: Isabella Lily Juliana (born 2002), Samuel Bernhard Louis (born 2004), and Benjamin Pieter Floris (born 2008).
According to a royal decree of 5 July 2000, the children were granted the family name van Vollenhoven, without titles.
In January 2026, Bernhard and Annette announced that they were to divorce.
Upon the announcement of the planned abdication of Queen Beatrix, which took place on 30 April 2013, it was also restated that after the abdication, the children of Princess Margriet and Pieter van Vollenhoven would no longer be eligible for the throne.
Health

Bernhard has been receiving treatment for Crohn's disease since 2002.
Ancestry

References

External links

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
  AssignClass (ad88cf95-fb94-436e-9f4e-aca522eac607)
 Call ID: ad88cf95-fb94-436e-9f4e-aca522eac607
  Args:
    source: :Beatrix
    type: :Woman
  AssignClass (79ea4a62-b32a-49da-8a8a-4a4cdcc6da21)
 Call ID: 79ea4a62-b32a-49da-8a8a-4a4cdcc6da21
  Args:
    type: :Woman
    source: :Margriet
  AssignClass (04ee5fe4-fba1-4944-89b1-9518e635b4ea)
 Call ID: 04ee5fe4-fba1-4944-89b1-9518e635b4ea
  Args:
    type: :Man
    source: :Pieter_van_Vollenhoven
  AssignClass (fdcc2ee6-0cd9-460e-8e6f-b707bb1e609d)
 Call ID: fdcc2ee6-0cd9-460e-8e6f-b707bb1e609d
  Args:
    source: :Bernhard_van_Vollenhoven
    type: :Man
  AddLiteral (ab03f221-3325-42c3-aaaf-0626c8529488)
 Call ID: ab03f221-3325-42c3-aaaf-0626c8529488
  Args:
    source: :Bernhard_van_Vollenhoven
    literal_type: xsd:integer
    literal_value: 1969
    relation: :hasBirthYear
  AddTriple (b4e4f917-9c27-40e5-8265-fbd70d362673)
 Call ID: b4e4f917-9c27-40e5-8265-fbd70d362673
  Args:
    source: :Bernhard_van_Vollenhoven
    target: :Margriet
    relation: :hasMother
  AddTriple (b1875f7c-77dc-466f-82ee-808314ece86b)
 Call ID: b1875f7c-77dc-466f-82ee-808314ece86b
  Args:
    source: :Bernhard_van_Vollenhoven
    relation: :hasFather
    target: :Pieter_van_Vollenhoven
  AssignClass (ff0053c6-ee44-415b-9de2-c8287e3a6a42)
 Call ID: ff0053c6-ee44-415b-9de2-c8287e3a6a42
  Args:
    type: :Man
    source: :Maurits_van_Vollenhoven
  AssignClass (41fdd02a-e7ed-40dd-9fb4-60ef547031ef)
 Call ID: 41fdd02a-e7ed-40dd-9fb4-60ef547031ef
  Args:
    type: :Man
    source: :Pieter-Christiaan_van_Vollenhoven
  AssignClass (69dc83d7-2462-4a48-bcc9-fafbb362a808)
 Call ID: 69dc83d7-2462-4a48-bcc9-fafbb362a808
  Args:
    source: :Floris_van_Vollenhoven
    type: :Man
  AddTriple (6ad1fedb-b6de-4c6d-8f0c-df5aef14715a)
 Call ID: 6ad1fedb-b6de-4c6d-8f0c-df5aef14715a
  Args:
    source: :Bernhard_van_Vollenhoven
    relation: :isBrotherOf
    target: :Maurits_van_Vollenhoven
  AddTriple (57d74f6a-625d-4eb1-9369-690aaf7a0b55)
 Call ID: 57d74f6a-625d-4eb1-9369-690aaf7a0b55
  Args:
    target: :Pieter-Christiaan_van_Vollenhoven
    relation: :isBrotherOf
    source: :Bernhard_van_Vollenhoven
  AddTriple (b14d2d7f-4827-47bb-a1a3-c2c3531adece)
 Call ID: b14d2d7f-4827-47bb-a1a3-c2c3531adece
  Args:
    relation: :isBrotherOf
    target: :Floris_van_Vollenhoven
    source: :Bernhard_van_Vollenhoven
  AssignClass (5169dba1-ff6f-41c9-9d5f-1a226ca0adb1)
 Call ID: 5169dba1-ff6f-41c9-9d5f-1a226ca0adb1
  Args:
    source: :Annette_Sekreve
    type: :Woman
  AddLiteral (5c54c2c1-6a38-48d3-89b8-81c617f8feb7)
 Call ID: 5c54c2c1-6a38-48d3-89b8-81c617f8feb7
  Args:
    literal_value: 1972
    relation: :hasBirthYear
    source: :Annette_Sekreve
    literal_type: xsd:integer
  AssignClass (bc519ecb-53be-47cc-9129-fa318688632a)
 Call ID: bc519ecb-53be-47cc-9129-fa318688632a
  Args:
    source: :Isabella_Lily_Juliana_van_Vollenhoven
    type: :Woman
  AssignClass (09c7e454-2294-47b2-bb8f-4b5889308d80)
 Call ID: 09c7e454-2294-47b2-bb8f-4b5889308d80
  Args:
    type: :Man
    source: :Samuel_Bernhard_Louis_van_Vollenhoven
  AssignClass (f6a6de3a-a94b-40bb-b51f-0d337915dae7)
 Call ID: f6a6de3a-a94b-40bb-b51f-0d337915dae7
  Args:
    source: :Benjamin_Pieter_Floris_van_Vollenhoven
    type: :Man
  AddLiteral (3ba78c52-6069-4752-96ec-095b513dacf1)
 Call ID: 3ba78c52-6069-4752-96ec-095b513dacf1
  Args:
    relation: :hasBirthYear
    literal_value: 2002
    literal_type: xsd:integer
    source: :Isabella_Lily_Juliana_van_Vollenhoven
  AddLiteral (a99eb636-0ed2-4f9e-b7c2-dc116eb36d0e)
 Call ID: a99eb636-0ed2-4f9e-b7c2-dc116eb36d0e
  Args:
    literal_value: 2004
    relation: :hasBirthYear
    source: :Samuel_Bernhard_Louis_van_Vollenhoven
    literal_type: xsd:integer
  AddLiteral (86f6c7cb-bb59-438c-85f5-427ae1d58fd1)
 Call ID: 86f6c7cb-bb59-438c-85f5-427ae1d58fd1
  Args:
    relation: :hasBirthYear
    literal_value: 2008
    literal_type: xsd:integer
    source: :Benjamin_Pieter_Floris_van_Vollenhoven
  AddTriple (56edba84-f992-4e72-86fd-0ce7b189485f)
 Call ID: 56edba84-f992-4e72-86fd-0ce7b189485f
  Args:
    relation: :hasFather
    target: :Bernhard_van_Vollenhoven
    source: :Isabella_Lily_Juliana_van_Vollenhoven
  AddTriple (b8e684ab-94e5-4cc4-bd75-26debd07a4e5)
 Call ID: b8e684ab-94e5-4cc4-bd75-26debd07a4e5
  Args:
    source: :Isabella_Lily_Juliana_van_Vollenhoven
    target: :Annette_Sekreve
    relation: :hasMother
  AddTriple (73f37632-758a-495c-8b1e-a9dea40d0b76)
 Call ID: 73f37632-758a-495c-8b1e-a9dea40d0b76
  Args:
    target: :Bernhard_van_Vollenhoven
    relation: :hasFather
    source: :Samuel_Bernhard_Louis_van_Vollenhoven
  AddTriple (9c767a74-bfb1-4a19-963d-a43ff08a2ffb)
 Call ID: 9c767a74-bfb1-4a19-963d-a43ff08a2ffb
  Args:
    source: :Samuel_Bernhard_Louis_van_Vollenhoven
    target: :Annette_Sekreve
    relation: :hasMother
  AddTriple (47b75014-cf05-49a6-9bd9-259a210c9d00)
 Call ID: 47b75014-cf05-49a6-9bd9-259a210c9d00
  Args:
    target: :Bernhard_van_Vollenhoven
    relation: :hasFather
    source: :Benjamin_Pieter_Floris_van_Vollenhoven
  AddTriple (7cb36d7c-97a6-4345-abc0-acd9a5227fd6)
 Call ID: 7cb36d7c-97a6-4345-abc0-acd9a5227fd6
  Args:
    source: :Benjamin_Pieter_Floris_van_Vollenhoven
    relation: :hasMother
    target: :Annette_Sekreve
  Finish (65e0d1e8-1a91-45b1-b940-e2a6fd26292d)
 Call ID: 65e0d1e8-1a91-45b1-b940-e2a6fd26292d
  Args: