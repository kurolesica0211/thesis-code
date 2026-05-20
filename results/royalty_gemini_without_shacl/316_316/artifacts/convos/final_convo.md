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
Descendants of Prince Felix and also members of the Grand Ducal Family of Luxembourg:


Princess Joan


Descendants of Prince René:


Princess Maria Pia


Princess Marina


Descendants of Prince Louis:


Prince RémyPrincess Elisabeth


Princess Chantal
Prince JeanPrincess Virginia


Princess Beatrix*


Princess Margriet*Pieter van Vollenhoven*


Prince Carlos, Duke of Parma and Piacenza (Carlos Xavier Bernardo Sixto Marie; born 27 January 1970) is the current Head of the House of Bourbon-Parma, which ruled the Duchy of Parma and Piacenza from 1748 to 1802 and from 1847 to 1859.
The eldest son of Carlos Hugo, Duke of Parma and Princess Irene of the Netherlands, Carlos is also a member of the Dutch royal family and the Dutch nobility with the style of "His Royal Highness" and the title of Prince Carlos de Bourbon de Parme.
Additionally, he is the Carlist pretender to the Spanish throne with the title Duke of Madrid.
In the French nobility, he bears the title "Prince de Borbon", and is the grand master of the Parmesan Sacred Military Constantinian Order of Saint George, the Order of Saint Louis for Civil Merit, the Order of Prohibited Legitimacy and the Order of St. George for Military Merit.
Early life

Prince Carlos Xavier Bernardo Sixto Marie of Bourbon-Parma was born in Nijmegen, The Netherlands on 27 January 1970 as the elder child and son of Carlos Hugo, Duke of Parma, and his wife Princess Irene of the Netherlands.
He has two younger sisters, Princess Margarita and Princess Carolina, and a younger brother, Prince Jaime.
At the time of his birth, his parents, Carlist Pretender to the Spanish throne, were expelled from Spain by the Franco regime since 20 December 1968, as Franco already did with his grandfather Prince Xavier of Bourbon-Parma and some members of his family on 25 November 1937.
Carlos spent his youth in several countries including the Netherlands, Spain, France, England, and the United States.
Together with his mother and his siblings, he then moved to Soestdijk Palace (Baarn) in the Netherlands.
He lived at the palace for a number of years with his maternal grandparents, Queen Juliana of the Netherlands and Prince Bernhard.
Education and career

Prince Carlos studied political science at Wesleyan University in Connecticut and demography and philosophy at Cambridge University in England; in 1995, he obtained a Postgraduate Degree (MPhil) in Demography at the Cambridge University.
After completing his studies, Carlos worked for the company ABN AMRO in Amsterdam, where he was involved with preparations for the introduction of the euro.
He has chaired the Foundation for Cooperation for the Economic Development of Latin America, was a member for eight years of the Council of CSR Netherlands, which ensures corporate social responsibility.
Duties and appearances

Dutch Royal House

Carlos is sometimes present at representative occasions concerning the Royal House of the Netherlands.
In 2003, he was involved, together with his aunt, Queen Beatrix, in the inauguration of the "Prince Claus Leerstoel", a professorship named after the Queen's husband, Prince Claus.
For example, he was one of the organizers of the wedding celebration of Prince Constantijn and Princess Laurentien.
In April 2013, Prince Carlos attended the inauguration of his cousin King Willem-Alexander and his wife Queen Maxima in Amsterdam.
In August 2019 he and his wife attended the funeral of his aunt Princess Christina of the Netherlands, sister of former Queen Beatrix, near Noordeinde Palace, The Hague.
His rights as the Carlist pretender

After the death of his father Carlos Hugo in 2010, Prince Carlos Xavier succeeded him as Duke of Madrid and Carlist Pretender to the Spanish throne.
He started to use the Carlist title of "Rey Don Carlos Javier I" (King Don Carlos Xavier I).
However, Carlos Xavier, in an interview with the newspaper La Vanguardia, said:


I don't set out dynastic lawsuits.
— Barcelona, October 11th, 2010

Duke of Parma

Prince Carlos became Duke of Parma and Piacenza and Head of the House of Bourbon-Parma after the death of his father on 18 August 2010, aged 80.
In 2016, at the baptism of Prince Carlos Enrique, Prince Carlos conferred on his son the title of "Principe di Piacenza" (Prince of Piacenza), which is the traditional title assigned to the Crown Prince of the House of Bourbon-Parma, the continuer of the dynasty, and future Duke of Parma and Piacenza.
In September 2017, the Duke of Parma named his daughter Princess Luisa as "Marchesa di Castell'Arquato" (Marquise of Castell'Arquato), and her younger sister Princess Cecilia was named as "Contessa di Berceto" (Countess of Berceto).
Prince Carlos has visited and regularly visits the lands of the former Duchy of Parma and Piacenza.
In September 2015, he was in Parma to grant the "Prince's Medal to Meritorious Men in silver" to the firefighters who distinguished themselves during the 2015 flood that struck the area.
At the end of September 2017, he presided over the General Chapter of the Knights of the House of Bourbon-Parma in Parma to confer the Ducal orders to those people who have achieved personal merits towards the Royal House; then he visited Palazzo della Pilotta.
In September 2018, he visited Parma to confer some honors of the Royal House and to visit the Church of Santa Maria della Steccata, together with the Royal Family.
Also, he was present at the inauguration of the opera season by attending a representation of the opera "Macbeth" at the Teatro Regio in Parma and made a visit to the Military Academy of Modena, received by the Commander.
As Duke of Parma, Prince Carlos is committed to preserving the memory of the lands and members and relatives of the dynasty: in July 2011 he was in Vienna to attend the funeral of Archduke Otto, the last Crown Prince of Austria-Hungary (son of Princess Zita of Bourbon-Parma, sister to Carlos' grandfather Prince Xavier) at the St. Stephen's Cathedral.
In August 2016, Prince Carlos was in Romania to attend the funeral of Queen Anne (née Princess of Bourbon-Parma as a daughter of Prince René, brother of Carlos' grandfather) in Curtea de Argeș.
At the funeral, Carlos represented also the Dutch Royal Family who was unable to attend.
In June 2018 he traveled to Prague to remember his ancestor Maria Amalia, Duchess of Parma, and to take part in the presentation of the book "Maria Amalia Duchess of Parma and Piacenza (1746–1804)" dedicated to the life of his ancestor, and later visited the Cathedral of San Vito in Prague to lay flowers on the tomb of Duchess Maria Amalia.
Personal life

Relationship with Brigitte Klynstra and son

Prince Carlos had a relationship with Brigitte Klynstra (born 10 January 1959), the stepdaughter of Count Adolph Roderik of Rechteren-Limpurg.
In December 2015, the then 18-year-old Carlos Klynstra started the legal procedure to attempt to change his surname to that of his biological father which would also allow him to use the title of "Prince".
The Duke of Parma opposed this on the basis that it was in contravention of the traditions of the House of Bourbon-Parma.
According to the judgement, Carlos Hugo will be entitled to be known as "Zijne Koninklijke Hoogheid Carlos Hugo Roderik Sybren prins de Bourbon de Parme" (His Royal Highness Prince Carlos Hugo Roderik Sybren of Bourbon-Parma); this will come only into effect once the Dutch king has signed the royal decree.
According to the press release of the Council of State of 28 February 2018, the name change does not mean that Klynstra is now also a member of the Royal House of  Bourbon-Parma.
Marriage to Annemarie Gualthérie van Weezel

On 7 October 2009, it was announced through his mother's private secretary that Prince Carlos would marry Annemarie Cecilia
Prince Carlos Hugo died shortly afterwards.
Her father was a member of the House of Representatives of the Netherlands for the Christian Democratic party, the Dutch ambassador to the Council of Europe in Strasbourg, and the ambassador to Luxembourg.
In Brussels, she met Prince Carlos for the first time.
On 2 August 2010, it was revealed that the health of his father, the Duke of Parma, was quickly deteriorating due to cancer.
As a consequence, the church wedding of the prince Carlos and his fiancée was delayed.
In a final announcement about his condition, the Duke confirmed Carlos as the next Head of the House of Bourbon-Parma.
Just before his death the old Duke of Parma named Annemarie as "Condesa de Molina" (Countess of Molina).
Prince Carlos's father died on 18 August 2010 in Barcelona, Spain, at the age of 80; Carlos subsequently became the next head of the House of Bourbon-Parma.
The new Duke of Parma and Annemarie were married on 20 November 2010 in La Cambre Abbey in Bruxelles.
The wedding was attended by Máxima, Princess of Orange, Willem-Alexander, Prince of Orange, Queen Beatrix of the Netherlands, Prince Jean of Luxembourg, Princess Astrid of Belgium, Prince Lorenz of Belgium and Duarte Pio, Duke of Braganza.
Together, they have two daughters and a son:


Titles, styles and honours

Titles and styles

Honours

Dynastic

As Head of the House of Bourbon-Parma, Carlos is Grand Master of four dynastic orders:


National

International

Ancestry

Notes

References

External links

2 gave up the title "Prince of the Netherlands, but still held the title "Prince of Orange-Nassau"
3 title granted by Royal Decree to descendants of Princess Irene



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
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

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

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

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

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



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (9d4aac7d-ea7f-42a2-8e81-d550ab75f64c)
 Call ID: 9d4aac7d-ea7f-42a2-8e81-d550ab75f64c
  Args:
    type: :Man
    source: Prince_Carlos
  AssignClass (800358a7-9d21-405b-9895-d73669f4ff5c)
 Call ID: 800358a7-9d21-405b-9895-d73669f4ff5c
  Args:
    source: Carlos_Hugo
    type: :Man
  AssignClass (a0b487fe-77cb-4ccd-87bc-44da9ff08660)
 Call ID: a0b487fe-77cb-4ccd-87bc-44da9ff08660
  Args:
    type: :Woman
    source: Princess_Irene
  AddTriple (eb07201e-2b87-402c-a86b-f04aba24a21f)
 Call ID: eb07201e-2b87-402c-a86b-f04aba24a21f
  Args:
    target: Carlos_Hugo
    source: Prince_Carlos
    relation: :hasFather
  AddTriple (8b351faf-c857-424e-ab2f-a4b89787d6af)
 Call ID: 8b351faf-c857-424e-ab2f-a4b89787d6af
  Args:
    relation: :hasMother
    source: Prince_Carlos
    target: Princess_Irene
  AssignClass (3976c27b-ea7a-4775-b44f-dcc96da0b348)
 Call ID: 3976c27b-ea7a-4775-b44f-dcc96da0b348
  Args:
    type: :Woman
    source: Princess_Margarita
  AssignClass (7bcaee51-96a6-446b-be14-8eeb3dc2583d)
 Call ID: 7bcaee51-96a6-446b-be14-8eeb3dc2583d
  Args:
    source: Princess_Carolina
    type: :Woman
  AssignClass (056db68c-7ded-4f58-a017-02f8bd887090)
 Call ID: 056db68c-7ded-4f58-a017-02f8bd887090
  Args:
    source: Prince_Jaime
    type: :Man
  AddTriple (99697538-4034-4e99-9658-963684eddec5)
 Call ID: 99697538-4034-4e99-9658-963684eddec5
  Args:
    target: Carlos_Hugo
    source: Princess_Margarita
    relation: :hasFather
  AddTriple (741721c8-e081-49a5-ad96-c132fe457768)
 Call ID: 741721c8-e081-49a5-ad96-c132fe457768
  Args:
    relation: :hasMother
    source: Princess_Margarita
    target: Princess_Irene
  AddTriple (2e27b899-49f9-44c3-95cb-58047d42d315)
 Call ID: 2e27b899-49f9-44c3-95cb-58047d42d315
  Args:
    target: Carlos_Hugo
    relation: :hasFather
    source: Princess_Carolina
  AddTriple (99c56ca8-3e0e-4b2a-97ba-9522e30bff7b)
 Call ID: 99c56ca8-3e0e-4b2a-97ba-9522e30bff7b
  Args:
    source: Princess_Carolina
    relation: :hasMother
    target: Princess_Irene
  AddTriple (dae2d067-dd4b-4240-bb6d-1415703bf187)
 Call ID: dae2d067-dd4b-4240-bb6d-1415703bf187
  Args:
    source: Prince_Jaime
    relation: :hasFather
    target: Carlos_Hugo
  AddTriple (93a59175-6622-4b9e-90b3-68fa3f66f87e)
 Call ID: 93a59175-6622-4b9e-90b3-68fa3f66f87e
  Args:
    target: Princess_Irene
    relation: :hasMother
    source: Prince_Jaime
  AssignClass (c5435c89-a1f5-4193-ba76-fcfa65538683)
 Call ID: c5435c89-a1f5-4193-ba76-fcfa65538683
  Args:
    source: Prince_Xavier
    type: :Man
  AddTriple (22536a78-6404-4b87-8cdb-63bb922f033f)
 Call ID: 22536a78-6404-4b87-8cdb-63bb922f033f
  Args:
    target: Prince_Xavier
    source: Carlos_Hugo
    relation: :hasFather
  AssignClass (e1bcc416-ed17-4a34-8d49-e1538c271441)
 Call ID: e1bcc416-ed17-4a34-8d49-e1538c271441
  Args:
    type: :Woman
    source: Annemarie_Gualthérie_van_Weezel
  AddTriple (1110e1da-6674-4eb1-95f6-e62bded6802c)
 Call ID: 1110e1da-6674-4eb1-95f6-e62bded6802c
  Args:
    relation: :hasRelation
    source: Prince_Carlos
    target: Annemarie_Gualthérie_van_Weezel
  AssignClass (114c6e1f-7aac-4294-b233-d1e04c1f6135)
 Call ID: 114c6e1f-7aac-4294-b233-d1e04c1f6135
  Args:
    type: :Man
    source: Prince_Carlos_Enrique
  AddTriple (e12b84d5-c4e6-42da-a714-9fb7d3cf5fbc)
 Call ID: e12b84d5-c4e6-42da-a714-9fb7d3cf5fbc
  Args:
    source: Prince_Carlos_Enrique
    relation: :hasFather
    target: Prince_Carlos
  AddTriple (c7d282ed-695b-4e15-85d1-ea1c47e100cf)
 Call ID: c7d282ed-695b-4e15-85d1-ea1c47e100cf
  Args:
    source: Prince_Carlos_Enrique
    relation: :hasMother
    target: Annemarie_Gualthérie_van_Weezel
  AssignClass (f7430b61-cb0f-4c68-9f58-5109582ec368)
 Call ID: f7430b61-cb0f-4c68-9f58-5109582ec368
  Args:
    type: :Woman
    source: Princess_Luisa
  AssignClass (e3c4bd93-1ee0-4f3a-bfd8-2fb3f28a0741)
 Call ID: e3c4bd93-1ee0-4f3a-bfd8-2fb3f28a0741
  Args:
    source: Princess_Cecilia
    type: :Woman
  AddTriple (59d0a1b0-b7cb-4508-9049-b248102dbcd8)
 Call ID: 59d0a1b0-b7cb-4508-9049-b248102dbcd8
  Args:
    target: Prince_Carlos
    relation: :hasFather
    source: Princess_Luisa
  AddTriple (d1f93d00-5bb2-407a-a736-5c41a1adf880)
 Call ID: d1f93d00-5bb2-407a-a736-5c41a1adf880
  Args:
    source: Princess_Luisa
    relation: :hasMother
    target: Annemarie_Gualthérie_van_Weezel
  AddTriple (ba67b794-77ec-4365-b02c-ef3a38f37b40)
 Call ID: ba67b794-77ec-4365-b02c-ef3a38f37b40
  Args:
    target: Prince_Carlos
    source: Princess_Cecilia
    relation: :hasFather
  AddTriple (6ba24a53-ebff-4017-8760-f6710135c9aa)
 Call ID: 6ba24a53-ebff-4017-8760-f6710135c9aa
  Args:
    relation: :hasMother
    source: Princess_Cecilia
    target: Annemarie_Gualthérie_van_Weezel
  AssignClass (fbf0cebc-7a9b-4048-9fdb-7be3c6b32b14)
 Call ID: fbf0cebc-7a9b-4048-9fdb-7be3c6b32b14
  Args:
    type: :Woman
    source: Princess_Joan
  AssignClass (c29d7bce-75d6-4028-8d3d-3b97edc1bfa1)
 Call ID: c29d7bce-75d6-4028-8d3d-3b97edc1bfa1
  Args:
    type: :Woman
    source: Princess_Maria_Pia
  AssignClass (78fb68c8-ea86-481e-a1c4-3f135b070105)
 Call ID: 78fb68c8-ea86-481e-a1c4-3f135b070105
  Args:
    source: Princess_Marina
    type: :Woman
  AssignClass (983e9d47-0403-43c0-8ae1-d37bcc2b8038)
 Call ID: 983e9d47-0403-43c0-8ae1-d37bcc2b8038
  Args:
    type: :Man
    source: Prince_Rémy
  AssignClass (aa985757-6281-4574-9266-16a34351d948)
 Call ID: aa985757-6281-4574-9266-16a34351d948
  Args:
    source: Princess_Elisabeth
    type: :Woman
  AssignClass (8de0c6d8-b6af-46af-9809-f8dfa1160387)
 Call ID: 8de0c6d8-b6af-46af-9809-f8dfa1160387
  Args:
    source: Princess_Chantal
    type: :Woman
  AssignClass (a0964550-0a78-4c75-ab9a-e9ae497ff3b5)
 Call ID: a0964550-0a78-4c75-ab9a-e9ae497ff3b5
  Args:
    type: :Man
    source: Prince_Jean
  AssignClass (b3f8849c-2130-4dff-b28c-cb1ce6c2f8d9)
 Call ID: b3f8849c-2130-4dff-b28c-cb1ce6c2f8d9
  Args:
    source: Princess_Virginia
    type: :Woman
  AssignClass (3dc88b14-e70d-47f8-b0ab-2a67b5a1b8cc)
 Call ID: 3dc88b14-e70d-47f8-b0ab-2a67b5a1b8cc
  Args:
    source: Princess_Beatrix
    type: :Woman
  AssignClass (cddcdfa9-fd60-44ba-b20b-420819557895)
 Call ID: cddcdfa9-fd60-44ba-b20b-420819557895
  Args:
    type: :Woman
    source: Princess_Margriet
  AssignClass (dcde6cca-fefe-4173-9b19-b723ac4299b7)
 Call ID: dcde6cca-fefe-4173-9b19-b723ac4299b7
  Args:
    type: :Man
    source: Pieter_van_Vollenhoven
  AssignClass (a9e6a657-9178-412d-8c0e-312aa1842207)
 Call ID: a9e6a657-9178-412d-8c0e-312aa1842207
  Args:
    source: Prince_Felix
    type: :Man
  AssignClass (ab26aa66-b330-4a5f-85e9-a01eb518d60d)
 Call ID: ab26aa66-b330-4a5f-85e9-a01eb518d60d
  Args:
    type: :Man
    source: Prince_René
  AssignClass (a3c7c454-97a6-45c3-a763-f161c111a286)
 Call ID: a3c7c454-97a6-45c3-a763-f161c111a286
  Args:
    source: Prince_Louis
    type: :Man
  AddTriple (06b5f3f8-9d3c-4709-9997-945647e2f7c1)
 Call ID: 06b5f3f8-9d3c-4709-9997-945647e2f7c1
  Args:
    relation: :hasChild
    source: Prince_Felix
    target: Princess_Joan
  AddTriple (99def86c-9260-484c-9349-eda43b1787ea)
 Call ID: 99def86c-9260-484c-9349-eda43b1787ea
  Args:
    target: Princess_Maria_Pia
    relation: :hasChild
    source: Prince_René
  AddTriple (c781c397-47f8-42bf-89fb-9d39c69a3aad)
 Call ID: c781c397-47f8-42bf-89fb-9d39c69a3aad
  Args:
    relation: :hasChild
    source: Prince_René
    target: Princess_Marina
  AddTriple (2fbbad4e-3d40-4ef4-9783-3940d387fe4d)
 Call ID: 2fbbad4e-3d40-4ef4-9783-3940d387fe4d
  Args:
    source: Prince_Louis
    relation: :hasChild
    target: Prince_Rémy
  AddTriple (da999dcf-b681-463c-853a-ef9ca1bad0e1)
 Call ID: da999dcf-b681-463c-853a-ef9ca1bad0e1
  Args:
    source: Prince_Louis
    relation: :hasChild
    target: Princess_Elisabeth
  AddTriple (26fb3144-f463-49d0-b58b-dde042d8f399)
 Call ID: 26fb3144-f463-49d0-b58b-dde042d8f399
  Args:
    target: Princess_Chantal
    source: Prince_Louis
    relation: :hasChild
  AddTriple (a8e2cd42-6276-4495-b1e4-62007e880ae7)
 Call ID: a8e2cd42-6276-4495-b1e4-62007e880ae7
  Args:
    source: Prince_Louis
    relation: :hasChild
    target: Prince_Jean
  AddTriple (df91260a-402b-4905-8660-cee12e8697da)
 Call ID: df91260a-402b-4905-8660-cee12e8697da
  Args:
    target: Princess_Virginia
    source: Prince_Louis
    relation: :hasChild
  Finish (ddb72e68-71f1-4146-b409-0eed724b0d78)
 Call ID: ddb72e68-71f1-4146-b409-0eed724b0d78
  Args: